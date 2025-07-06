from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.group_service import (
    create_group,
    get_all_groups,
    get_group_by_id,
    get_user_groups,
    update_group,
    delete_group,
    join_group,
    leave_group
)
from app.services.user_service import get_user_by_id

groups_bp = Blueprint("groups", __name__, url_prefix="/api/v1/groups")


# Create a new group
@groups_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_group():
    user_id = get_jwt_identity()
    data = request.get_json()

    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "Group name is required"}), 400

    group = create_group(name=name, description=description, creator_id=user_id)
    return jsonify({
        "message": "Group created successfully",
        "group": {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "creator_id": group.creator_id
        }
    }), 201


#  Get all groups
@groups_bp.route("/", methods=["GET"])
@jwt_required()
def list_groups():
    groups = get_all_groups()
    return jsonify([
        {
            "id": g.id,
            "name": g.name,
            "description": g.description,
            "creator_id": g.creator_id
        }
        for g in groups
    ]), 200


# Get groups joined by current user
@groups_bp.route("/mine", methods=["GET"])
@jwt_required()
def my_groups():
    user_id = get_jwt_identity()
    groups = get_user_groups(user_id)
    return jsonify([
        {
            "id": g.id,
            "name": g.name,
            "description": g.description,
            "creator_id": g.creator_id
        }
        for g in groups
    ]), 200


#  Join a group
@groups_bp.route("/<int:group_id>/join", methods=["POST"])
@jwt_required()
def join_group_route(group_id):
    user_id = get_jwt_identity()
    joined = join_group(group_id, user_id)
    if not joined:
        return jsonify({"error": "Already a member or group not found"}), 400
    return jsonify({"message": f"Joined group {group_id} successfully"}), 200


#  Leave a group
@groups_bp.route("/<int:group_id>/leave", methods=["POST"])
@jwt_required()
def leave_group_route(group_id):
    user_id = get_jwt_identity()
    left = leave_group(group_id, user_id)
    if not left:
        return jsonify({"error": "Not a member or group not found"}), 400
    return jsonify({"message": f"Left group {group_id} successfully"}), 200


#  Update a group (creator or admin only)
@groups_bp.route("/<int:group_id>", methods=["PUT"])
@jwt_required()
def update_group_route(group_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    group = get_group_by_id(group_id)

    if not group:
        return jsonify({"error": "Group not found"}), 404

    if group.creator_id != user_id and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    updated = update_group(group_id, data.get("name"), data.get("description"))

    return jsonify({
        "message": "Group updated successfully",
        "group": {
            "id": updated.id,
            "name": updated.name,
            "description": updated.description
        }
    }), 200


#  Delete a group (creator or admin only)
@groups_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_group_route(group_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    group = get_group_by_id(group_id)

    if not group:
        return jsonify({"error": "Group not found"}), 404

    if group.creator_id != user_id and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    delete_group(group_id)
    return jsonify({"message": f"Group {group_id} deleted successfully"}), 200
