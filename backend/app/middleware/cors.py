from flask_cors import CORS

def configure_cors(app):
    """
    Enable CORS for the Flask app.

    Adjust origins and headers based on your frontend domain or development needs.
    """
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},  # You can replace "*" with your frontend URL
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
