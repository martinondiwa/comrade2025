from flask import Flask
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

    # Register blueprints (API modules)
    app.register_blueprint(auth.bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users.bp, url_prefix='/api/v1/users')
    app.register_blueprint(campuses.bp, url_prefix='/api/v1/campuses')
    app.register_blueprint(posts.bp, url_prefix='/api/v1/posts')
    app.register_blueprint(comments.bp, url_prefix='/api/v1/comments')
    app.register_blueprint(likes.bp, url_prefix='/api/v1/likes')
    app.register_blueprint(media.bp, url_prefix='/api/v1/media')
    app.register_blueprint(groups.bp, url_prefix='/api/v1/groups')
    app.register_blueprint(events.bp, url_prefix='/api/v1/events')
    app.register_blueprint(notifications.bp, url_prefix='/api/v1/notifications')

    return app

