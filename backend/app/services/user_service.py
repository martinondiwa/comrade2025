from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import IntegrityError


def create_user(username, email, password, **extra_fields):
    """
    Create a new user with hashed password.
    Returns the user instance or raises an exception on failure.
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


def get_user_by_id(user_id):
    """
    Retrieve a user by their unique ID.
    Returns User instance or None.
    """
    return User.query.get(user_id)


def get_user_by_email(email):
    """
    Retrieve a user by their email.
    Returns User instance or None.
    """
    return User.query.filter_by(email=email).first()


def get_user_by_username(username):
    """
    Retrieve a user by their username.
    Returns User instance or None.
    """
    return User.query.filter_by(username=username).first()


def verify_password(user, password):
    """
    Verify if the provided password matches the user's stored password hash.
    Returns True or False.
    """
    if not user:
        return False
    return check_password_hash(user.password_hash, password)


def update_user_profile(user_id, **update_fields):
    """
    Update user profile fields (like bio, profile_picture, etc).
    Returns updated User instance or None if user not found.
    """
    user = get_user_by_id(user_id)
    if not user:
        return None
    for key, value in update_fields.items():
        setattr(user, key, value)
    db.session.commit()
    return user


def search_users(query, limit=10, offset=0):
    """
    Search users by username or email with pagination.
    Returns list of User instances.
    """
    search = "%{}%".format(query)
    return User.query.filter(
        (User.username.ilike(search)) | (User.email.ilike(search))
    ).limit(limit).offset(offset).all()


def deactivate_user(user_id):
    """
    Soft delete or deactivate a user account.
    Here, assume there's an 'is_active' field.
    Returns True if successful, False if user not found.
    """
    user = get_user_by_id(user_id)
    if not user:
        return False
    user.is_active = False
    db.session.commit()
    return True
