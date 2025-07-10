from app.extensions import db
from datetime import datetime


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # Nullable for system notifications
    notification_type = db.Column(db.String(100), nullable=False)  # e.g., 'like', 'comment', 'follow', 'event'
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    recipient = db.relationship(
        "User",
        foreign_keys=[recipient_id],
        back_populates="notifications"
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_notifications"
    )

    def __repr__(self):
        return f"<Notification id={self.id} recipient={self.recipient_id} type={self.notification_type}>"

    def to_dict(self):
        return {
            "id": self.id,
            "recipient_id": self.recipient_id,
            "sender_id": self.sender_id,
            "notification_type": self.notification_type,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat(),
        }
