from datetime import datetime
from typing import List, Optional, Dict, Any

from app.extensions import db
from app.models.post import Post
from app.models.user import User
from app.models.campus import Campus
from app.models.group import Group
from app.models.media import Media
from app.models.like import Like
from app.utils.pagination import paginate_query


class PostService:
    def create_post(self, author_id: int, content: str, campus_id: Optional[int] = None,
                    group_id: Optional[int] = None, media_ids: Optional[List[int]] = None) -> Post:
        """
        Create a new post.
        
        Args:
            author_id (int): User ID of post author.
            content (str): Text content of the post.
            campus_id (int, optional): Campus ID if post is campus-specific.
            group_id (int, optional): Group ID if post belongs to a group.
            media_ids (List[int], optional): List of media IDs attached to the post.
        
        Returns:
            Post: Created Post instance.
        
        Raises:
            ValueError: If invalid campus or group ID.
        """
        # Optional validations
        if campus_id and not Campus.query.get(campus_id):
            raise ValueError("Invalid campus_id")
        if group_id and not Group.query.get(group_id):
            raise ValueError("Invalid group_id")

        post = Post(
            author_id=author_id,
            content=content,
            campus_id=campus_id,
            group_id=group_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        if media_ids:
            media_items = Media.query.filter(Media.id.in_(media_ids)).all()
            post.media = media_items

        db.session.add(post)
        db.session.commit()
        return post

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        """
        Retrieve a post by its ID.
        
        Args:
            post_id (int): Post ID.
        
        Returns:
            Post or None: Post instance or None if not found.
        """
        return Post.query.get(post_id)

    def update_post(self, post_id: int, author_id: int, new_content: Optional[str] = None,
                    media_ids: Optional[List[int]] = None) -> Post:
        """
        Update a post's content or media (author only).
        
        Args:
            post_id (int): Post ID.
            author_id (int): User ID requesting update (must be author).
            new_content (str, optional): New content text.
            media_ids (List[int], optional): Updated list of media IDs.
        
        Returns:
            Post: Updated Post instance.
        
        Raises:
            ValueError: If post not found or unauthorized.
        """
        post = self.get_post_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        if post.author_id != author_id:
            raise PermissionError("Unauthorized to update this post")

        if new_content is not None:
            post.content = new_content
        if media_ids is not None:
            media_items = Media.query.filter(Media.id.in_(media_ids)).all()
            post.media = media_items

        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    def delete_post(self, post_id: int, author_id: int) -> None:
        """
        Delete a post (author only).
        
        Args:
            post_id (int): Post ID.
            author_id (int): User ID requesting deletion (must be author).
        
        Raises:
            ValueError: If post not found or unauthorized.
        """
        post = self.get_post_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        if post.author_id != author_id:
            raise PermissionError("Unauthorized to delete this post")

        db.session.delete(post)
        db.session.commit()

    def _apply_filters(self, query, campus_id: Optional[int] = None,
                       group_id: Optional[int] = None, author_id: Optional[int] = None):
        """
        Helper to apply filtering conditions to a query.
        """
        if campus_id is not None:
            query = query.filter(Post.campus_id == campus_id)
        if group_id is not None:
            query = query.filter(Post.group_id == group_id)
        if author_id is not None:
            query = query.filter(Post.author_id == author_id)
        return query

    def get_posts(self, page: int = 1, per_page: int = 20,
                  campus_id: Optional[int] = None, group_id: Optional[int] = None,
                  author_id: Optional[int] = None, order_desc: bool = True) -> Dict[str, Any]:
        """
        Retrieve posts with optional filters and pagination.
        
        Args:
            page (int): Page number.
            per_page (int): Items per page.
            campus_id (int, optional): Filter posts by campus.
            group_id (int, optional): Filter posts by group.
            author_id (int, optional): Filter posts by author.
            order_desc (bool): Whether to order posts descending by created_at.
        
        Returns:
            Dict[str, Any]: Pagination result with 'items' (List[Post]) and pagination metadata.
        """
        query = Post.query

        query = self._apply_filters(query, campus_id, group_id, author_id)

        order_col = Post.created_at.desc() if order_desc else Post.created_at.asc()
        query = query.order_by(order_col)

        return paginate_query(query, page, per_page)

    def count_likes(self, post_id: int) -> int:
        """
        Count how many likes a post has.
        
        Args:
            post_id (int): Post ID.
        
        Returns:
            int: Number of likes.
        """
        return Like.query.filter_by(post_id=post_id).count()

    def user_liked_post(self, user_id: int, post_id: int) -> bool:
        """
        Check if a user has liked a post.
        
        Args:
            user_id (int): User ID.
            post_id (int): Post ID.
        
        Returns:
            bool: True if user liked the post, else False.
        """
        return Like.query.filter_by(user_id=user_id, post_id=post_id).first() is not None
