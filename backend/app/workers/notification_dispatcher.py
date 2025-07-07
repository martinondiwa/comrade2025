from app.workers import celery
from app.extensions import db
from app.models.notification import Notification
from datetime import datetime

@celery.task(name="dispatch_notification")
def dispatch_notification(
    recipient_id: int,
    sender_id: int,
    type: str,
    message: str,
    target_type: str = None,
    target_id: int = None
):
    """
    Asynchronously creates and saves a notification.
    """
    try:
        notification = Notification(
            recipient_id=recipient_id,
            sender_id=sender_id,
            type=type,
            message=message,
            target_type=target_type,
            target_id=target_id,
            created_at=datetime.utcnow(),
            read=False
        )
        db.session.add(notification)
        db.session.commit()
        print(f"[✅] Notification dispatched to user {recipient_id}")

    except Exception as e:
        db.session.rollback()
        print(f"[❌] Failed to dispatch notification: {str(e)}")
