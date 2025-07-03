
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Initialize Flask extensions (no app context yet)
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
