from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.campus_service import (
    get_all_campuses,
    get_campus_by_id,
    create_campus,
    update_campus,
    delete_campus
)
from app.services.user_service import get_user_by_id

campus_bp = Blueprint("campuses", __name__, url_prefix="/api/v1/campuses")


# Utility: Check if current user is admin
def admin_required(fn):
    from functools import wraps

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_user_by_id(get_jwt_identity())
        if not user or not user.is_admin:
            return jsonify({"message": "Admin access only"}), 403
        return fn(*args, **kwargs)
    return wrapper


# ✅ List all campuses
@campus_bp.route("/", methods=["GET"])
@jwt_required()
def list_campuses():
    campuses = get_all_campuses()
    result = [
        {
            "id": c.id,
            "name": c.name,
            "location": c.location,
            "description": c.description
        }
        for c in campuses
    ]
    return jsonify(result), 200


# ✅ Get one campus
@campus_bp.route("/<int:campus_id>", methods=["GET"])
@jwt_required()
def get_one_campus(campus_id):
    campus = get_campus_by_id(campus_id)
    if not campus:
        return jsonify({"error": "Campus not found"}), 404

    return jsonify({
        "id": campus.id,
        "name": campus.name,
        "location": campus.location,
        "description": campus.description
    }), 200


# ✅ Create new campus (Admin only)
@campus_bp.route("/", methods=["POST"])
@admin_required
def create_new_campus():
    data = request.get_json()
    name = data.get("name")
    location = data.get("location")
    description = data.get("description")

    if not name or not location:
        return jsonify({"error": "Name and location are required"}), 400

    campus = create_campus(name, location, description)
    return jsonify({
        "message": "Campus created successfully",
        "campus": {
            "id": campus.id,
            "name": campus.name,
            "location": campus.location,
            "description": campus.description
        }
    }), 201


# ✅ Update campus (Admin only)
@campus_bp.route("/<int:campus_id>", methods=["PUT"])
@admin_required
def update_existing_campus(campus_id):
    campus = get_campus_by_id(campus_id)
    if not campus:
        return jsonify({"error": "Campus not found"}), 404

    data = request.get_json()
    name = data.get("name", campus.name)
    location = data.get("location", campus.location)
    description = data.get("description", campus.description)

    updated = update_campus(campus_id, name, location, description)
    return jsonify({
        "message": "Campus updated successfully",
        "campus": {
            "id": updated.id,
            "name": updated.name,
            "location": updated.location,
            "description": updated.description
        }
    }), 200


# ✅ Delete campus (Admin only)
@campus_bp.route("/<int:campus_id>", methods=["DELETE"])
@admin_required
def delete_existing_campus(campus_id):
    campus = get_campus_by_id(campus_id)
    if not campus:
        return jsonify({"error": "Campus not found"}), 404

    delete_campus(campus_id)
    return jsonify({"message": f"Campus {campus_id} deleted successfully"}), 200
