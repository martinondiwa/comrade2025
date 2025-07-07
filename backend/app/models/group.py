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
    creator = db.relationship("User", backref=db.backref("created_groups", lazy="dynamic"))
    members = db.relationship(
        "GroupMembership", back_populates="group", cascade="all, delete-orphan"
    )
    posts = db.relationship("Post", backref="group", lazy=True)

    def __repr__(self):
        return f"<Group {self.name} by User {self.creator_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creator_id": self.creator_id,
            "created_at": self.created_at.isoformat(),
            "members_count": len(self.members),
            # You could add more details here if needed
        }
