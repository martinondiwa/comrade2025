from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.extensions import db
from app.utils import jwt_utils
from datetime import datetime


class AuthService:
    def __init__(self):
        self.jwt_expiration = current_app.config.get('JWT_EXPIRATION_DELTA', 3600)

    def register_user(self, username: str, email: str, password: str, full_name: str = "") -> dict:
        """
        Register a new user.
        """
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            created_at=datetime.utcnow()
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Username or email already exists")

        return {
            "message": "User registered successfully",
            "user_id": new_user.id
        }

    def login_user(self, email_or_username: str, password: str) -> dict:
        """
        Authenticate user and return JWT token.
        """
        user = User.query.filter(
            (User.email == email_or_username) | (User.username == email_or_username)
        ).first()

        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid credentials")

        token = jwt_utils.generate_token(user_id=user.id)

        return {
            "access_token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
            }
        }

    def verify_token(self, token: str) -> dict:
        """
        Decode and verify JWT token.
        """
        payload = jwt_utils.decode_token(token)
        if not payload:
            raise ValueError("Invalid or expired token")

        user_id = payload.get("user_id")
        user = User.query.get(user_id)

        if not user:
            raise ValueError("User not found")

        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }

    def reset_password(self, email: str, new_password: str) -> dict:
        """
        Reset password for a user.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")

        user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        return {
            "message": "Password reset successful"
        }

    def update_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        """
        Change user password after verifying old password.
        """
        user = User.query.get(user_id)
        if not user or not check_password_hash(user.password_hash, old_password):
            raise ValueError("Invalid old password")

        user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        return {
            "message": "Password updated successfully"
        }
