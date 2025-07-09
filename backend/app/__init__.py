from flask import Flask, jsonify
from .extensions import db, jwt, migrate
from .config import development
from .api.v1 import auth, users, campuses, posts, comments, likes, media, groups, events, notifications

def create_app(config_class=development.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints with their correct names
    app.register_blueprint(auth.auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users.users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(campuses.campus_bp, url_prefix='/api/v1/campuses')
    app.register_blueprint(posts.posts_bp, url_prefix='/api/v1/posts')
    app.register_blueprint(comments.comments_bp, url_prefix='/api/v1/comments')
    app.register_blueprint(likes.likes_bp, url_prefix='/api/v1/likes')
    app.register_blueprint(media.media_bp, url_prefix='/api/v1/media')
    app.register_blueprint(groups.groups_bp, url_prefix='/api/v1/groups')
    app.register_blueprint(events.events_bp, url_prefix='/api/v1/events')
    app.register_blueprint(notifications.notifications_bp, url_prefix='/api/v1/notifications')

    # Add a simple root route
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Comrade API. Use /api/v1/* endpoints."})

    return app
