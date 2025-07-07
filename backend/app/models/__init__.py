from app.extensions import db

# Import all models to ensure they are registered with SQLAlchemy's metadata
from .user import User
from .campus import Campus
from .post import Post
from .comment import Comment
from .like import Like
from .media import Media
from .group import Group
from .group_membership import GroupMembership
from .event import Event
from .chat_message import ChatMessage
from .notification import Notification
from .follow import Follow

__all__ = [
    "db",
    "User",
    "Campus",
    "Post",
    "Comment",
    "Like",
    "Media",
    "Group",
    "GroupMembership",
    "Event",
    "ChatMessage",
    "Notification",
    "Follow"
]
