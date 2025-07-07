from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_service import PostService

posts_bp = Blueprint("posts", __name__, url_prefix="/api/v1/posts")

post_service = PostService()  # create an instance of PostService

@posts_bp.route("/", methods=["GET"])
@jwt_required()
def list_posts():
    campus_id = request.args.get("campus_id", type=int)
    user_id = request.args.get("user_id", type=int)
    
    try:
        if campus_id:
            posts = post_service.get_posts(campus_id=campus_id)
        elif user_id:
            posts = post_service.get_posts(author_id=user_id)
        else:
            posts = post_service.get_posts()
        
        # posts is a pagination dict, get items list
        posts_list = [post.to_dict() for post in posts['items']]
        return jsonify({"status": "success", "data": posts_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@posts_bp.route("/<int:post_id>", methods=["GET"])
@jwt_required()
def get_post(post_id):
    post = post_service.get_post_by_id(post_id)
    if not post:
        return jsonify({"status": "error", "message": "Post not found."}), 404
    return jsonify({"status": "success", "data": post.to_dict()}), 200

@posts_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_post():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    try:
        post = post_service.create_post(
            author_id=user_id,
            content=data.get("content"),
            campus_id=data.get("campus_id"),
            group_id=data.get("group_id"),
            media_ids=data.get("media_ids"),
        )
        return jsonify({"status": "success", "data": post.to_dict()}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@posts_bp.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def edit_post(post_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    try:
        post = post_service.update_post(
            post_id=post_id,
            author_id=user_id,
            new_content=data.get("content"),
            media_ids=data.get("media_ids"),
        )
        return jsonify({"status": "success", "data": post.to_dict()}), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except PermissionError as e:
        return jsonify({"status": "error", "message": str(e)}), 403

@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def remove_post(post_id):
    user_id = get_jwt_identity()
    try:
        post_service.delete_post(post_id=post_id, author_id=user_id)
        return jsonify({"status": "success", "message": "Post deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except PermissionError as e:
        return jsonify({"status": "error", "message": str(e)}), 403

# For like/unlike, you need to implement similar methods in PostService, or implement here

# Dummy example implementations:
@posts_bp.route("/<int:post_id>/like", methods=["POST"])
@jwt_required()
def like(post_id):
    user_id = get_jwt_identity()
    # Implement like_post in PostService or handle here
    # Example:
    try:
        # post_service.like_post(user_id, post_id) # If implemented
        return jsonify({"status": "success", "message": "Post liked"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@posts_bp.route("/<int:post_id>/unlike", methods=["POST"])
@jwt_required()
def unlike(post_id):
    user_id = get_jwt_identity()
    try:
        # post_service.unlike_post(user_id, post_id) # If implemented
        return jsonify({"status": "success", "message": "Post unliked"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
