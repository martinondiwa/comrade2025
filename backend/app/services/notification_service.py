from datetime import datetime
from app.extensions import db
from app.models.notification import Notification
from app.models.user import User
from app.workers.notification_dispatcher import enqueue_notification_dispatch


class NotificationService:
    def create_notification(
        self,
        recipient_id: int,
        sender_id: int,
        message: str,
        notif_type: str = None,
        target_type: str = None,
        target_id: int = None,
        link: str = None
    ) -> Notification:
        """
        Create a new notification and optionally dispatch it async.
        """
        notification = Notification(
            user_id=recipient_id,
            message=message,
            link=link,
            type=notif_type,
            created_at=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification)
        db.session.commit()

        # Asynchronously enqueue notification (e.g., email, push, websocket)
        enqueue_notification_dispatch.delay(
            recipient_id=recipient_id,
            sender_id=sender_id,
            type=notif_type,
            message=message,
            target_type=target_type,
            target_id=target_id
        )

        return notification

    def get_user_notifications(self, user_id: int, unread_only: bool = False, limit: int = 50):
        """
        Fetch notifications for a user.
        """
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        return notifications

    def mark_as_read(self, notification_id: int, user_id: int) -> Notification:
        """
        Mark a specific notification as read.
        """
        notification = Notification.query.get(notification_id)
        if not notification:
            raise ValueError("Notification not found.")
        if notification.user_id != user_id:
            raise PermissionError("Unauthorized action.")
        if not notification.is_read:
            notification.is_read = True
            db.session.commit()
        return notification

    def delete_notification(self, notification_id: int, user_id: int) -> None:
        """
        Delete a notification owned by user.
        """
        notification = Notification.query.get(notification_id)
        if not notification:
            raise ValueError("Notification not found.")
        if notification.user_id != user_id:
            raise PermissionError("Unauthorized action.")
        db.session.delete(notification)
        db.session.commit()


# Create a single instance for module-level usage
notification_service = NotificationService()

# Convenience module-level functions to call on the instance

def create_notification(*args, **kwargs):
    return notification_service.create_notification(*args, **kwargs)

def get_user_notifications(*args, **kwargs):
    return notification_service.get_user_notifications(*args, **kwargs)

def mark_as_read(*args, **kwargs):
    return notification_service.mark_as_read(*args, **kwargs)

def delete_notification(*args, **kwargs):
    return notification_service.delete_notification(*args, **kwargs)

# Standalone utility functions

def mark_notification_as_read(notification_id: int):
    """
    Mark a single notification as read.
    """
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
        return True
    return False

def mark_all_notifications_as_read(user_id: int) -> int:
    """
    Mark all unread notifications for the user as read.
    Returns the number of updated records.
    """
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
    if not notifications:
        return 0
    for notif in notifications:
        notif.is_read = True
    db.session.commit()
    return len(notifications)
