from flask import Blueprint

v1 = Blueprint('v1', __name__)

# Import your api v1 modules here
from . import (
    auth,
    users,
    campuses,
    posts,
    comments,
    likes,
    media,
    groups,
    chat,
    events,
    notifications,
    admin
)

# Register blueprints with the v1 blueprint
v1.register_blueprint(auth.auth_bp)         # from auth.py, blueprint variable: auth_bp
v1.register_blueprint(users.users_bp)       # from users.py, blueprint variable: users_bp
v1.register_blueprint(campuses.campuses_bp) # from campuses.py, blueprint variable: campuses_bp
v1.register_blueprint(posts.posts_bp)       # from posts.py, blueprint variable: posts_bp
v1.register_blueprint(comments.comments_bp) # from comments.py, blueprint variable: comments_bp
v1.register_blueprint(likes.likes_bp)       # from likes.py, blueprint variable: likes_bp
v1.register_blueprint(media.media_bp)       # from media.py, blueprint variable: media_bp
v1.register_blueprint(groups.groups_bp)     # from groups.py, blueprint variable: groups_bp
v1.register_blueprint(chat.chat_bp)         # from chat.py, blueprint variable: chat_bp
v1.register_blueprint(events.events_bp)     # from events.py, blueprint variable: events_bp
v1.register_blueprint(notifications.notifications_bp) # from notifications.py, blueprint variable: notifications_bp
v1.register_blueprint(admin.admin_bp)       # from admin.py, blueprint variable: admin_bp
