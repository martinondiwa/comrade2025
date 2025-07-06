from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.like_service import (
    like_post,
    unlike_post,
    get_like_count,
    has_liked_post
)
from app.services.post_service import get_post_by_id

likes_bp = Blueprint("likes", __name__, url_prefix="/api/v1/likes")


# ✅ Like a post
@likes_bp.route("/<int:post_id>/like", methods=["POST"])
@jwt_required()
def like(post_id):
    user_id = get_jwt_identity()

    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    success = like_post(post_id, user_id)
    if not success:
        return jsonify({"message": "You already liked this post"}), 400

    return jsonify({"message": f"Post {post_id} liked successfully"}), 200


# ✅ Unlike a post
@likes_bp.route("/<int:post_id>/unlike", methods=["POST"])
@jwt_required()
def unlike(post_id):
    user_id = get_jwt_identity()

    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    success = unlike_post(post_id, user_id)
    if not success:
        return jsonify({"message": "You haven't liked this post yet"}), 400

    return jsonify({"message": f"Post {post_id} unliked successfully"}), 200


# ✅ Get like count for a post
@likes_bp.route("/<int:post_id>/count", methods=["GET"])
@jwt_required()
def like_count(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    count = get_like_count(post_id)
    return jsonify({"post_id": post_id, "likes": count}), 200


# ✅ Check if user liked a post
@likes_bp.route("/<int:post_id>/status", methods=["GET"])
@jwt_required()
def like_status(post_id):
    user_id = get_jwt_identity()
    liked = has_liked_post(post_id, user_id)
    return jsonify({"liked": liked}), 200
