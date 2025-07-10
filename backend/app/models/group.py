from app.extensions import db
from datetime import datetime


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    creator = db.relationship("User", back_populates="created_groups")

    members = db.relationship(
        "GroupMembership",
        back_populates="group",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    posts = db.relationship(
        "Post",
        back_populates="group",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Group {self.name} by User {self.creator_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creator_id": self.creator_id,
            "created_at": self.created_at.isoformat(),
            "members_count": self.members.count(),  # Better than len() with lazy="dynamic"
        }
