from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_service import CommentService
from app.services.user_service import get_user_by_id
from app.services.post_service import get_post_by_id

comments_bp = Blueprint("comments", __name__, url_prefix="/api/v1/comments")

# Instantiate the service
comment_service = CommentService()


# Create a comment on a post
@comments_bp.route("/<int:post_id>", methods=["POST"])
@jwt_required()
def post_comment(post_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Comment text is required"}), 400

    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comment = comment_service.create_comment(post_id=post_id, user_id=user.id, text=text)

    return jsonify({
        "message": "Comment added successfully",
        "comment": {
            "id": comment.id,
            "text": comment.text,
            "user_id": comment.user_id,
            "post_id": comment.post_id,
            "timestamp": comment.timestamp.isoformat()
        }
    }), 201


# Get all comments on a post
@comments_bp.route("/post/<int:post_id>", methods=["GET"])
@jwt_required()
def get_comments(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comments = comment_service.get_comments_by_post(post_id)

    return jsonify([
        {
            "id": c.id,
            "text": c.text,
            "user_id": c.user_id,
            "post_id": c.post_id,
            "timestamp": c.timestamp.isoformat()
        }
        for c in comments
    ]), 200


# Update own comment
@comments_bp.route("/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_user_comment(comment_id):
    user_id = get_jwt_identity()
    comment = comment_service.get_comment_by_id(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if comment.user_id != user_id:
        return jsonify({"error": "You can only update your own comments"}), 403

    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    updated = comment_service.update_comment(comment_id, text)

    return jsonify({
        "message": "Comment updated successfully",
        "comment": {
            "id": updated.id,
            "text": updated.text,
            "timestamp": updated.timestamp.isoformat()
        }
    }), 200


# Delete comment (admin or owner)
@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_user_comment(comment_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    comment = comment_service.get_comment_by_id(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if comment.user_id != user_id and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    comment_service.delete_comment(comment_id)

    return jsonify({"message": f"Comment {comment_id} deleted successfully"}), 200
