
from datetime import datetime
from typing import List, Optional

from app.extensions import db
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User

class CommentService:
    @staticmethod
    def create_comment(author_id: int, post_id: int, content: str) -> Comment:
        """
        Create a new comment for a post.
        """
        post = Post.query.get(post_id)
        if not post:
            raise ValueError("Post not found")
        
        comment = Comment(
            author_id=author_id,
            post_id=post_id,
            content=content,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def get_comment_by_id(comment_id: int) -> Optional[Comment]:
        return Comment.query.get(comment_id)

    @staticmethod
    def get_comments_by_post(post_id: int, limit: int = 20, offset: int = 0) -> List[Comment]:
        return Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).limit(limit).offset(offset).all()

    @staticmethod
    def update_comment(comment_id: int, author_id: int, content: str) -> Optional[Comment]:
        comment = Comment.query.get(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.author_id != author_id:
            raise PermissionError("Unauthorized to update this comment")

        comment.content = content
        comment.updated_at = datetime.utcnow()
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment_id: int, author_id: int) -> None:
        comment = Comment.query.get(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.author_id != author_id:
            raise PermissionError("Unauthorized to delete this comment")

        db.session.delete(comment)
        db.session.commit()
