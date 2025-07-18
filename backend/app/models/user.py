from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(150), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_image_url = db.Column(db.String(512), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey("campuses.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships (simple ones declared here)
    campus = db.relationship("Campus", back_populates="users")
    comments = db.relationship("Comment", back_populates="user", lazy="dynamic")
    created_events = db.relationship("Event", back_populates="creator", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_image_url": self.profile_image_url,
            "campus_id": self.campus_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_email:
            data["email"] = self.email
        return data


# --- Late binding of relationships to resolve circular imports ---
from app.models.media import Media  # updated import from media.py
from app.models.chat_message import ChatMessage
from app.models.follow import Follow
from app.models.group_membership import GroupMembership
from app.models.like import Like
from app.models.post import Post
from app.models.group import Group
from app.models.notification import Notification  # Add Notification import


User.likes = db.relationship("Like", back_populates="user", lazy="dynamic")
User.posts = db.relationship("Post", back_populates="user", lazy="dynamic")
User.media_files = db.relationship("Media", back_populates="uploader", lazy="dynamic")
User.created_groups = db.relationship("Group", back_populates="creator", lazy="dynamic")

User.group_memberships = db.relationship(
    "GroupMembership",
    back_populates="user",
    cascade="all, delete-orphan",
    lazy="dynamic"
)

User.sent_messages = db.relationship(
    "ChatMessage",
    foreign_keys=lambda: [ChatMessage.sender_id],
    back_populates="sender",
    lazy="dynamic"
)

User.received_messages = db.relationship(
    "ChatMessage",
    foreign_keys=lambda: [ChatMessage.receiver_id],
    back_populates="receiver",
    lazy="dynamic"
)

User.following = db.relationship(
    "Follow",
    foreign_keys=lambda: [Follow.follower_id],
    back_populates="follower",
    lazy="dynamic"
)

User.followers = db.relationship(
    "Follow",
    foreign_keys=lambda: [Follow.followed_id],
    back_populates="followed",
    lazy="dynamic"
)

# **Add these relationships for notifications**

User.notifications = db.relationship(
    "Notification",
    foreign_keys="[Notification.recipient_id]",
    back_populates="recipient",
    lazy="dynamic",
    cascade="all, delete-orphan"
)

User.sent_notifications = db.relationship(
    "Notification",
    foreign_keys="[Notification.sender_id]",
    back_populates="sender",
    lazy="dynamic",
    cascade="all, delete-orphan"
)
