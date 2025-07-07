from app.workers import celery
from app.extensions import mail
from flask_mail import Message
from flask import current_app


@celery.task(name="send_email")
def send_email(subject, recipients, body, html=None, sender=None):
    """
    Asynchronously sends an email using Flask-Mail.

    Args:
        subject (str): Subject line
        recipients (list): List of recipient email addresses
        body (str): Plain text content
        html (str, optional): HTML content
        sender (str, optional): From address (defaults to MAIL_DEFAULT_SENDER)
    """
    try:
        sender = sender or current_app.config.get("MAIL_DEFAULT_SENDER")

        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html,
            sender=sender
        )
        mail.send(msg)
        print(f"[✅] Email sent to {recipients}")

    except Exception as e:
        print(f"[❌] Failed to send email to {recipients}: {str(e)}")
