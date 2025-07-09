from flask import Blueprint

v1 = Blueprint('v1', __name__)

def register_v1_blueprints():
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

    v1.register_blueprint(auth.auth_bp)
    v1.register_blueprint(users.users_bp)
    v1.register_blueprint(campuses.campuses_bp)
    v1.register_blueprint(posts.posts_bp)
    v1.register_blueprint(comments.comments_bp)
    v1.register_blueprint(likes.likes_bp)
    v1.register_blueprint(media.media_bp)
    v1.register_blueprint(groups.groups_bp)
    v1.register_blueprint(chat.chat_bp)
    v1.register_blueprint(events.events_bp)
    v1.register_blueprint(notifications.notifications_bp)
    v1.register_blueprint(admin.admin_bp)
