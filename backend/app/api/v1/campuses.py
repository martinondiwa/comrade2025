from flask import Blueprint, request, jsonify
#from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

from app.services.campus_service import CampusService
from app.services.user_service import UserService  

campus_bp = Blueprint("campuses", __name__, url_prefix="/api/v1/campuses")


# Decorator: Check if the current user is an admin
def admin_required(fn):
    @wraps(fn)
    #@jwt_required()
    def wrapper(*args, **kwargs):
        user = UserService.get_user_by_id(get_jwt_identity())  
        if not user or not user.is_admin:
            return jsonify({"message": "Admin access only"}), 403
        return fn(*args, **kwargs)
    return wrapper


# Route: List all campuses
@campus_bp.route("/", methods=["GET"])
#@jwt_required()
def list_campuses():
    campuses = CampusService.get_all_campuses()
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


# Route: Get one campus by ID
@campus_bp.route("/<int:campus_id>", methods=["GET"])
#@jwt_required()
def get_one_campus(campus_id):
    campus = CampusService.get_campus_by_id(campus_id)
    if not campus:
        return jsonify({"error": "Campus not found"}), 404

    return jsonify({
        "id": campus.id,
        "name": campus.name,
        "location": campus.location,
        "description": campus.description
    }), 200


# Route: Create a new campus (admin only)
@campus_bp.route("/", methods=["POST"])
#@admin_required
def create_new_campus():
    data = request.get_json() or {}
    name = data.get("name")
    location = data.get("location")
    description = data.get("description")

    if not name or not location:
        return jsonify({"error": "Name and location are required"}), 400

    campus = CampusService.create_campus(name, location, description)
    return jsonify({
        "message": "Campus created successfully",
        "campus": {
            "id": campus.id,
            "name": campus.name,
            "location": campus.location,
            "description": campus.description
        }
    }), 201


# Route: Update existing campus (admin only)
@campus_bp.route("/<int:campus_id>", methods=["PUT"])
#@admin_required
def update_existing_campus(campus_id):
    campus = CampusService.get_campus_by_id(campus_id)
    if not campus:
        return jsonify({"error": "Campus not found"}), 404

    data = request.get_json() or {}
    name = data.get("name", campus.name)
    location = data.get("location", campus.location)
    description = data.get("description", campus.description)

    updated = CampusService.update_campus(campus_id, name, location, description)
    return jsonify({
        "message": "Campus updated successfully",
        "campus": {
            "id": updated.id,
            "name": updated.name,
            "location": updated.location,
            "description": updated.description
        }
    }), 200


# Route: Delete a campus (admin only)
@campus_bp.route("/<int:campus_id>", methods=["DELETE"])
#@admin_required
def delete_existing_campus(campus_id):
    campus = CampusService.get_campus_by_id(campus_id)
    if not campus:
        return jsonify({"error": "Campus not found"}), 404

    CampusService.delete_campus(campus_id)
    return jsonify({"message": f"Campus {campus_id} deleted successfully"}), 200
