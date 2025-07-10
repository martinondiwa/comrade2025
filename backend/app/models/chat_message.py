from app.extensions import db
from datetime import datetime


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships (optional, for easier joins)
    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_messages"
    )
    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_messages"
    )

    def __repr__(self):
        return f"<ChatMessage id={self.id} from={self.sender_id} to={self.receiver_id} at={self.timestamp}>"

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "is_read": self.is_read,
        }
