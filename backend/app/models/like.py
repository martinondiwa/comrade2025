from app.extensions import db
from datetime import datetime


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref=db.backref("likes", cascade="all, delete-orphan"))
    post = db.relationship("Post", backref=db.backref("likes", cascade="all, delete-orphan"))

    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="uq_user_post_like"),
    )

    def __repr__(self):
        return f"<Like user_id={self.user_id} post_id={self.post_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat(),
        }
