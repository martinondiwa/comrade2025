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
        return Post.query.get(post_id)

    def update_post(self, post_id: int, author_id: int, new_content: Optional[str] = None,
                    media_ids: Optional[List[int]] = None) -> Post:
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
        post = self.get_post_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        if post.author_id != author_id:
            raise PermissionError("Unauthorized to delete this post")

        db.session.delete(post)
        db.session.commit()

    def _apply_filters(self, query, campus_id: Optional[int] = None,
                       group_id: Optional[int] = None, author_id: Optional[int] = None):
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
        query = Post.query
        query = self._apply_filters(query, campus_id, group_id, author_id)
        order_col = Post.created_at.desc() if order_desc else Post.created_at.asc()
        query = query.order_by(order_col)
        return paginate_query(query, page, per_page)

    def count_likes(self, post_id: int) -> int:
        return Like.query.filter_by(post_id=post_id).count()

    def user_liked_post(self, user_id: int, post_id: int) -> bool:
        return Like.query.filter_by(user_id=user_id, post_id=post_id).first() is not None

    def like_post(self, user_id: int, post_id: int) -> None:
        if self.user_liked_post(user_id, post_id):
            return
        like = Like(user_id=user_id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    def unlike_post(self, user_id: int, post_id: int) -> None:
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()


# --------------------------------------
# Instance and Wrapper Functions
# --------------------------------------

post_service = PostService()


def get_post_by_id(post_id):
    return post_service.get_post_by_id(post_id)


def create_post(author_id, data):
    post = post_service.create_post(
        author_id=author_id,
        content=data.get("content"),
        campus_id=data.get("campus_id"),
        group_id=data.get("group_id"),
        media_ids=data.get("media_ids", [])
    )
    return _wrap_response(post)


def update_post(user_id, post_id, data):
    try:
        updated = post_service.update_post(
            post_id=post_id,
            author_id=user_id,
            new_content=data.get("content"),
            media_ids=data.get("media_ids", [])
        )
        return {
            "message": "Post updated successfully",
            "post": {
                "id": updated.id,
                "content": updated.content,
                "updated_at": updated.updated_at.isoformat()
            }
        }, 200
    except PermissionError as e:
        return {"error": str(e)}, 403
    except Exception as e:
        return {"error": str(e)}, 400


def delete_post(user_id, post_id):
    try:
        post_service.delete_post(post_id, user_id)
        return {"message": f"Post {post_id} deleted successfully"}, 200
    except PermissionError as e:
        return {"error": str(e)}, 403
    except Exception as e:
        return {"error": str(e)}, 400


def get_all_posts():
    result = post_service.get_posts()
    return [post.as_dict() for post in result["items"]]


def get_posts_by_user(user_id):
    result = post_service.get_posts(author_id=user_id)
    return [post.as_dict() for post in result["items"]]


def get_posts_by_campus(campus_id):
    result = post_service.get_posts(campus_id=campus_id)
    return [post.as_dict() for post in result["items"]]


def like_post(user_id, post_id):
    post_service.like_post(user_id, post_id)
    return {"message": "Post liked successfully"}, 200


def unlike_post(user_id, post_id):
    post_service.unlike_post(user_id, post_id)
    return {"message": "Post unliked successfully"}, 200


def _wrap_response(post):
    return {
        "message": "Post created successfully",
        "post": {
            "id": post.id,
            "author_id": post.author_id,
            "content": post.content,
            "created_at": post.created_at.isoformat()
        }
    }, 201
