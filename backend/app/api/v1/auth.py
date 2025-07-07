from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.services.user_service import UserService
from app.extensions import db
import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


# Register a new user
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = UserService.get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 409

    try:
        user = UserService.create_user(username=username, email=email, password=password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 201


# Login and get JWT tokens
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = UserService.get_user_by_email(email)
    if not user or not UserService.verify_password(user, password):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is inactive. Contact admin."}), 403

    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=2))
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }), 200


# Refresh Access Token
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({
        "access_token": access_token
    }), 200


# Get current logged-in user profile
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "is_active": user.is_active
    }), 200
