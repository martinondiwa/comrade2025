from flask import jsonify
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, Unauthorized, Forbidden, InternalServerError

def register_error_handlers(app):
    """
    Register global error handlers for clean API responses.
    """

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handles built-in HTTP exceptions (like 400, 404)."""
        response = {
            "status": "error",
            "message": e.description,
            "code": e.code
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        """Handles all uncaught exceptions."""
        app.logger.exception("Unhandled exception occurred")

        response = {
            "status": "error",
            "message": "An unexpected error occurred. Please try again later.",
            "code": 500
        }
        return jsonify(response), 500

    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify({
            "status": "error",
            "message": "Bad request. Please check your input.",
            "code": 400
        }), 400

    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({
            "status": "error",
            "message": "Unauthorized access.",
            "code": 401
        }), 401

    @app.errorhandler(Forbidden)
    def handle_forbidden(e):
        return jsonify({
            "status": "error",
            "message": "You do not have permission to perform this action.",
            "code": 403
        }), 403

    @app.errorhandler(NotFound)
    def handle_not_found(e):
        return jsonify({
            "status": "error",
            "message": "The requested resource was not found.",
            "code": 404
        }), 404

    @app.errorhandler(InternalServerError)
    def handle_server_error(e):
        return jsonify({
            "status": "error",
            "message": "Internal server error. Our engineers are looking into it.",
            "code": 500
        }), 500
