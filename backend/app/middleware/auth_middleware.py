from flask import request, g
import logging
from flask_jwt_extended import verify_jwt_in_request_optional, get_jwt_identity

logger = logging.getLogger(__name__)


def register_auth_middleware(app):
    """
    Register request middleware that runs before every request.
    Can be used for:
    - Logging
    - Tracing authenticated user
    - Auditing
    """

    @app.before_request
    def before_request_func():
        """
        Middleware that runs before each request.
        It sets `g.current_user_id` if a valid JWT is provided.
        """
        verify_jwt_in_request_optional()
        g.current_user_id = get_jwt_identity()

        logger.debug(f"Request Path: {request.path}")
        logger.debug(f"Method: {request.method}")
        logger.debug(f"Authenticated User ID: {g.current_user_id}")

    @app.after_request
    def after_request_func(response):
        """
        Middleware that runs after each request.
        You can use this for metrics, logging, etc.
        """
        response.headers['X-Comrade-App'] = 'Backend'
        return response
