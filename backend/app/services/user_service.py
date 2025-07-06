from app.models.user import User
from app.extensions import db

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_all_users():
    return User.query.all()

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
