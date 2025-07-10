from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Only needed if you're using lambda references to Message columns
from app.models.message import Message


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

    # Relationships
    campus = db.relationship("Campus", back_populates="users")
    comments = db.relationship('Comment', back_populates='user', lazy='dynamic')
    created_events = db.relationship('Event', back_populates='creator', lazy='dynamic')

    group_memberships = db.relationship(
        "GroupMembership",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    sent_messages = db.relationship(
        "Message",
        foreign_keys=lambda: [Message.sender_id],
        back_populates="sender",
        lazy="dynamic"
    )

    received_messages = db.relationship(
        "Message",
        foreign_keys=lambda: [Message.receiver_id],
        back_populates="receiver",
        lazy="dynamic"
    )

    following = db.relationship(
        'Follow',
        foreign_keys=lambda: [db.foreign('Follow.follower_id')],
        back_populates='follower',
        lazy='dynamic'
    )

    followers = db.relationship(
        'Follow',
        foreign_keys=lambda: [db.foreign('Follow.followed_id')],
        back_populates='followed',
        lazy='dynamic'
    )

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
