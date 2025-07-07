from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.extensions import db


class UserService:
    @staticmethod
    def create_user(username, email, password, **extra_fields):
        """
        Creates a new user with hashed password.
        """
        password_hash = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            **extra_fields
        )
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("User with that email or username already exists.")

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def verify_password(user, password):
        if not user:
            return False
        return check_password_hash(user.password_hash, password)

    @staticmethod
    def update_user_profile(user_id, **update_fields):
        user = User.query.get(user_id)
        if not user:
            return None
        for key, value in update_fields.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def search_users(query, limit=10, offset=0):
        search = f"%{query}%"
        return User.query.filter(
            (User.username.ilike(search)) | (User.email.ilike(search))
        ).limit(limit).offset(offset).all()

    @staticmethod
    def deactivate_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        user.is_active = False  # Ensure your User model has this field
        db.session.commit()
        return True
