from datetime import datetime
from app.extensions import db
from app.models.notification import Notification
from app.models.user import User
from app.workers.notification_dispatcher import enqueue_notification_dispatch



class NotificationService:
    def create_notification(self, user_id: int, message: str, link: str = None, notif_type: str = None) -> Notification:
        """
        Create a new notification for a user.
        
        Args:
            user_id (int): The ID of the user to notify.
            message (str): Notification message/content.
            link (str, optional): URL or app route linked to notification.
            notif_type (str, optional): Type/category of notification (e.g., "like", "comment").
        
        Returns:
            Notification: The created Notification object.
        """
        notification = Notification(
            user_id=user_id,
            message=message,
            link=link,
            type=notif_type,
            created_at=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification)
        db.session.commit()

        # Optionally enqueue async dispatch (email, push, websocket)
        enqueue_notification_dispatch(notification.id)

        return notification

    def get_user_notifications(self, user_id: int, unread_only: bool = False, limit: int = 50):
        """
        Fetch notifications for a user.
        
        Args:
            user_id (int): User ID to fetch notifications for.
            unread_only (bool): If True, fetch only unread notifications.
            limit (int): Max number of notifications to return.
        
        Returns:
            List[Notification]: List of notification objects.
        """
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        return notifications

    def mark_as_read(self, notification_id: int, user_id: int) -> Notification:
        """
        Mark a specific notification as read.
        
        Args:
            notification_id (int): Notification ID.
            user_id (int): User ID, to ensure ownership.
        
        Returns:
            Notification: Updated notification object.
        
        Raises:
            ValueError: If notification not found or unauthorized.
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
        
        Args:
            notification_id (int): Notification ID.
            user_id (int): User ID to verify ownership.
        
        Raises:
            ValueError: If notification not found.
            PermissionError: If user unauthorized.
        """
        notification = Notification.query.get(notification_id)
        if not notification:
            raise ValueError("Notification not found.")
        if notification.user_id != user_id:
            raise PermissionError("Unauthorized action.")
        db.session.delete(notification)
        db.session.commit()
