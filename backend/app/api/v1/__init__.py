from flask import Blueprint

v1 = Blueprint('v1', __name__)

from .auth import auth_bp
from .users import users_bp
from .campuses import campus_bp
from .posts import posts_bp
from .comments import comments_bp
from .likes import likes_bp
from .media import media_bp
from .groups import groups_bp
from .chat import chat_bp
from .events import events_bp
from .notifications import notifications_bp
from .admin import admin_bp

v1.register_blueprint(auth_bp)
v1.register_blueprint(users_bp)
v1.register_blueprint(campus_bp)
v1.register_blueprint(posts_bp)
v1.register_blueprint(comments_bp)
v1.register_blueprint(likes_bp)
v1.register_blueprint(media_bp)
v1.register_blueprint(groups_bp)
v1.register_blueprint(chat_bp)
v1.register_blueprint(events_bp)
v1.register_blueprint(notifications_bp)
v1.register_blueprint(admin_bp)
