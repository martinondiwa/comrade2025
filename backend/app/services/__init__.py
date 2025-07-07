"""
Service Layer Initialization
----------------------------
This module initializes all service modules used throughout the application.
It provides a centralized access point to import business logic services
like user management, posts, authentication, groups, media handling, etc.

Each service is structured to encapsulate business rules and logic, keeping
routes (API) and models clean and maintainable.
"""

# Import individual service modules for easy access
from .auth_service import AuthService
from .user_service import UserService
from .post_service import PostService
from .group_service import GroupService
from .campus_service import CampusService
from .media_service import MediaService
from .event_service import EventService
from .notification_service import NotificationService
from .chat_service import ChatService

# Expose them at package level for easy imports
__all__ = [
    "auth_service",
    "user_service",
    "post_service",
    "group_service",
    "campus_service",
    "media_service",
    "event_service",
    "notification_service",
    "chat_service",
]
