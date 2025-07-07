
from app.extensions import db
from app.models.like import Like

def like_post(post_id, user_id):
    existing_like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
    if existing_like:
        return False
    new_like = Like(post_id=post_id, user_id=user_id)
    db.session.add(new_like)
    db.session.commit()
    return True

def unlike_post(post_id, user_id):
    like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
    if not like:
        return False
    db.session.delete(like)
    db.session.commit()
    return True

def get_like_count(post_id):
    return Like.query.filter_by(post_id=post_id).count()

def has_liked_post(post_id, user_id):
    return Like.query.filter_by(post_id=post_id, user_id=user_id).first() is not None
