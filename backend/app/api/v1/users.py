from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import (
    create_user,
    get_user_by_id,
    update_user,
    delete_user,
    get_all_users,
    search_users_by_name,
)

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@users_bp.route("/", methods=["GET"])
@jwt_required()
def list_users():
    users = get_all_users()
    return jsonify({"status": "success", "data": users}), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404
    return jsonify({"status": "success", "data": user}), 200


@users_bp.route("/", methods=["POST"])
def register_user():
    data = request.get_json()
    result, status = create_user(data)
    return jsonify(result), status


@users_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user_details(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"status": "error", "message": "Unauthorized."}), 403

    data = request.get_json()
    result, status = update_user(user_id, data)
    return jsonify(result), status


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_account(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"status": "error", "message": "Unauthorized."}), 403

    result, status = delete_user(user_id)
    return jsonify(result), status


@users_bp.route("/search", methods=["GET"])
@jwt_required()
def search_users():
    query = request.args.get("q", "")
    users = search_users_by_name(query)
    return jsonify({"status": "success", "data": users}), 200
