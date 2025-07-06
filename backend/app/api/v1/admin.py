from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import get_user_by_id, get_all_users, delete_user
from app.services.post_service import get_all_posts, delete_post
from app.extensions import db
from app.models.user import User
from app.models.post import Post

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


# Helper: Ensure the requester is admin
def admin_required(fn):
    from functools import wraps

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = get_user_by_id(user_id)
        if not user or not user.is_admin:
            return jsonify({"message": "Admin access only"}), 403
        return fn(*args, **kwargs)
    return wrapper


# Route: Get all users
@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    users = get_all_users()
    user_data = [{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "is_admin": u.is_admin
    } for u in users]
    return jsonify(user_data), 200


# Route: Delete a user
@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def remove_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    delete_user(user_id)
    return jsonify({"message": f"User {user_id} deleted."}), 200


# Route: Get all posts
@admin_bp.route("/posts", methods=["GET"])
@admin_required
def list_posts():
    posts = get_all_posts()
    post_data = [{
        "id": p.id,
        "content": p.content,
        "author_id": p.user_id,
        "timestamp": p.created_at.isoformat()
    } for p in posts]
    return jsonify(post_data), 200


# Route: Delete a post
@admin_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@admin_required
def remove_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": f"Post {post_id} deleted."}), 200


# Route: Platform statistics
@admin_bp.route("/stats", methods=["GET"])
@admin_required
def get_stats():
    user_count = User.query.count()
    post_count = Post.query.count()
    return jsonify({
        "total_users": user_count,
        "total_posts": post_count
    }), 200
