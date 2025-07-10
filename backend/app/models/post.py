from app.extensions import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    author = db.relationship("User", backref=db.backref("posts", lazy="dynamic"))
    campus = db.relationship("Campus", back_populates="posts")
    group = db.relationship("Group", backref=db.backref("posts", lazy="dynamic"))
    comments = db.relationship(
        "Comment", backref="post", cascade="all, delete-orphan", lazy="dynamic"
    )
    likes = db.relationship(
        "Like", backref="post", cascade="all, delete-orphan", lazy="dynamic"
    )
    media = db.relationship(
        "Media", backref="post", cascade="all, delete-orphan", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Post id={self.id} user_id={self.user_id} created_at={self.created_at}>"

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "campus_id": self.campus_id,
            "group_id": self.group_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "comments_count": self.comments.count(),
            "likes_count": self.likes.count(),
            "media": [m.to_dict() for m in self.media],
        }
