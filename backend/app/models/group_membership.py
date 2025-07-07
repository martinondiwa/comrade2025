from app.extensions import db
from datetime import datetime


class GroupMembership(db.Model):
    __tablename__ = "group_memberships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="member")  # e.g. member, admin, moderator
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref=db.backref("group_memberships", cascade="all, delete-orphan"))
    group = db.relationship("Group", back_populates="members")

    __table_args__ = (
        db.UniqueConstraint("user_id", "group_id", name="uq_user_group"),
    )

    def __repr__(self):
        return f"<GroupMembership user_id={self.user_id} group_id={self.group_id} role={self.role}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "group_id": self.group_id,
            "role": self.role,
            "joined_at": self.joined_at.isoformat(),
        }
