import os
from app import create_app

# Load config based on environment variable
config_type = os.getenv("FLASK_ENV", "development")

if config_type == "production":
    from app.config.production import Config
elif config_type == "testing":
    from app.config.testing import Config
else:
    from app.config.development import Config

app = create_app(config_class=Config)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
