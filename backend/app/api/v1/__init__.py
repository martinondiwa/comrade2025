# File: backend/app/api/v1/__init__.py

from flask import Blueprint

# This Blueprint will be used to register all version 1 API routes
v1 = Blueprint('v1', __name__)

# Import and register all individual feature modules
from . import auth, users, campuses, posts, comments, likes, media, groups, chat, events, notifications, admin

# Each module (e.g., auth.py) must define a Blueprint object named `bp`
v1.register_blueprint(auth.bp, url_prefix='/auth')
v1.register_blueprint(users.bp, url_prefix='/users')
v1.register_blueprint(campuses.bp, url_prefix='/campuses')
v1.register_blueprint(posts.bp, url_prefix='/posts')
v1.register_blueprint(comments.bp, url_prefix='/comments')
v1.register_blueprint(likes.bp, url_prefix='/likes')
v1.register_blueprint(media.bp, url_prefix='/media')
v1.register_blueprint(groups.bp, url_prefix='/groups')
v1.register_blueprint(chat.bp, url_prefix='/chat')
v1.register_blueprint(events.bp, url_prefix='/events')
v1.register_blueprint(notifications.bp, url_prefix='/notifications')
v1.register_blueprint(admin.bp, url_prefix='/admin')
