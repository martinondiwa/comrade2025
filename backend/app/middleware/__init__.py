from flask import Flask
from app.middleware.cors import configure_cors
from app.middleware.error_handler import register_error_handlers
from app.middleware.auth_middleware import register_auth_middleware


def register_middlewares(app: Flask):
    """
    Register all middleware layers for the Flask app.
    This includes:
    - CORS setup
    - Error handling
    - Custom auth/request middlewares
    """
    configure_cors(app)
    register_error_handlers(app)
    register_auth_middleware(app)
