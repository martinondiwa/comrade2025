from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_service import (
    create_post,
    get_post_by_id,
    update_post,
    delete_post,
    get_all_posts,
    get_posts_by_user,
    get_posts_by_campus,
    like_post,
    unlike_post,
)

posts_bp = Blueprint("posts", __name__, url_prefix="/api/v1/posts")


@posts_bp.route("/", methods=["GET"])
@jwt_required()
def list_posts():
    campus_id = request.args.get("campus_id")
    user_id = request.args.get("user_id")

    if campus_id:
        posts = get_posts_by_campus(campus_id)
    elif user_id:
        posts = get_posts_by_user(user_id)
    else:
        posts = get_all_posts()

    return jsonify({"status": "success", "data": posts}), 200


@posts_bp.route("/<int:post_id>", methods=["GET"])
@jwt_required()
def get_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"status": "error", "message": "Post not found."}), 404
    return jsonify({"status": "success", "data": post}), 200


@posts_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = create_post(user_id, data)
    return jsonify(result), status


@posts_bp.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def edit_post(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = update_post(user_id, post_id, data)
    return jsonify(result), status


@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def remove_post(post_id):
    user_id = get_jwt_identity()
    result, status = delete_post(user_id, post_id)
    return jsonify(result), status


@posts_bp.route("/<int:post_id>/like", methods=["POST"])
@jwt_required()
def like(post_id):
    user_id = get_jwt_identity()
    result, status = like_post(user_id, post_id)
    return jsonify(result), status


@posts_bp.route("/<int:post_id>/unlike", methods=["POST"])
@jwt_required()
def unlike(post_id):
    user_id = get_jwt_identity()
    result, status = unlike_post(user_id, post_id)
    return jsonify(result), status
