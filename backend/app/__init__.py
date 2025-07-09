from flask import Flask
from .extensions import db, jwt, migrate
from .config import development

# Import the wrapper blueprint that includes all v1 modules
from app.api.v1 import v1 as api_v1_blueprint

def create_app(config_class=development.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register all API v1 blueprints at once
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
