from flask import Blueprint

# Main API v1 Blueprint
v1 = Blueprint('v1', __name__)

# Import and register sub-blueprints
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

# Register all blueprints to v1
blueprints = [
    auth_bp,
    users_bp,
    campus_bp,
    posts_bp,
    comments_bp,
    likes_bp,
    media_bp,
    groups_bp,
    chat_bp,
    events_bp,
    notifications_bp,
    admin_bp,
]

for bp in blueprints:
    v1.register_blueprint(bp)
