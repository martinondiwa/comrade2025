from flask import Blueprint, request, jsonify
#from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.user_service import UserService

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@users_bp.route("/", methods=["GET"])
#@jwt_required()
def list_users():
    users = UserService.search_users("")  # Can add pagination later
    return jsonify({
        "status": "success",
        "data": [user.to_dict() for user in users]
    }), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
#@jwt_required()
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404
    return jsonify({"status": "success", "data": user.to_dict()}), 200


@users_bp.route("/", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    try:
        user = UserService.create_user(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password")
        )
        return jsonify({"status": "success", "data": user.to_dict()}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@users_bp.route("/<int:user_id>", methods=["PUT"])
#@jwt_required()
def update_user_details(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"status": "error", "message": "Unauthorized."}), 403

    data = request.get_json() or {}
    user = UserService.update_user_profile(user_id, **data)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404
    return jsonify({"status": "success", "data": user.to_dict()}), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
#@jwt_required()
def delete_user_account(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"status": "error", "message": "Unauthorized."}), 403

    success = UserService.deactivate_user(user_id)
    if not success:
        return jsonify({"status": "error", "message": "User not found or already inactive."}), 404
    return jsonify({"status": "success", "message": "User deactivated successfully."}), 200


@users_bp.route("/search", methods=["GET"])
#@jwt_required()
def search_users():
    query = request.args.get("q", "")
    users = UserService.search_users(query)
    return jsonify({
        "status": "success",
        "data": [user.to_dict() for user in users]
    }), 200
