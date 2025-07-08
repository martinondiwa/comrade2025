from datetime import datetime
from app.extensions import db
from app.models.chat_message import ChatMessage
from app.models.user import User
from sqlalchemy import or_, and_

class ChatService:
    def send_message(self, sender_id: int, recipient_id: int, content: str) -> dict:
        """
        Send a message from one user to another.
        """
        sender = User.query.get(sender_id)
        recipient = User.query.get(recipient_id)

        if not sender or not recipient:
            raise ValueError("Sender or recipient does not exist.")

        message = ChatMessage(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content,
            timestamp=datetime.utcnow(),
            is_read=False
        )

        db.session.add(message)
        db.session.commit()

        return {
            "message_id": message.id,
            "timestamp": message.timestamp.isoformat(),
            "status": "sent"
        }

    def get_conversation(self, user1_id: int, user2_id: int, limit: int = 50, offset: int = 0) -> list:
        """
        Fetch recent messages between two users, ordered chronologically.
        """
        messages = ChatMessage.query.filter(
            or_(
                and_(ChatMessage.sender_id == user1_id, ChatMessage.recipient_id == user2_id),
                and_(ChatMessage.sender_id == user2_id, ChatMessage.recipient_id == user1_id)
            )
        ).order_by(ChatMessage.timestamp.desc()) \
         .limit(limit).offset(offset).all()

        return [
            {
                "id": msg.id,
                "sender_id": msg.sender_id,
                "recipient_id": msg.recipient_id,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "is_read": msg.is_read
            }
            for msg in reversed(messages)
        ]

    def mark_as_read(self, message_id: int, reader_id: int) -> dict:
        """
        Mark a specific message as read.
        """
        message = ChatMessage.query.get(message_id)
        if not message:
            raise ValueError("Message not found.")

        if message.recipient_id != reader_id:
            raise PermissionError("You can only mark your own received messages as read.")

        message.is_read = True
        db.session.commit()

        return {
            "message": "Message marked as read.",
            "message_id": message.id
        }

    def delete_message(self, message_id: int, requester_id: int) -> dict:
        """
        Delete a message (only by sender).
        """
        message = ChatMessage.query.get(message_id)
        if not message:
            raise ValueError("Message not found.")

        if message.sender_id != requester_id:
            raise PermissionError("Only the sender can delete this message.")

        db.session.delete(message)
        db.session.commit()

        return {
            "message": "Message deleted successfully.",
            "message_id": message_id
        }
