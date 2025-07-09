from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import mark_notification_as_read
from app.services.notification_service import (
    get_user_notifications,
    mark_notification_as_read,
    mark_all_notifications_as_read,
    delete_notification
)

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")


#  Get logged-in user's notifications (paginated)
@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_notifications():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("limit", 10, type=int)

    notifications, total = get_user_notifications(user_id, page, per_page)

    return jsonify({
        "notifications": [
            {
                "id": n.id,
                "type": n.type,
                "message": n.message,
                "is_read": n.is_read,
                "related_id": n.related_id,
                "created_at": n.created_at.isoformat()
            } for n in notifications
        ],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total
        }
    }), 200


# Mark a single notification as read
@notifications_bp.route("/<int:notification_id>/read", methods=["POST"])
@jwt_required()
def read_single(notification_id):
    user_id = get_jwt_identity()
    success = mark_notification_as_read(user_id, notification_id)
    if not success:
        return jsonify({"error": "Notification not found or unauthorized"}), 404
    return jsonify({"message": "Notification marked as read"}), 200


# Mark all as read
@notifications_bp.route("/read-all", methods=["POST"])
@jwt_required()
def read_all():
    user_id = get_jwt_identity()
    mark_all_notifications_as_read(user_id)
    return jsonify({"message": "All notifications marked as read"}), 200


# Delete a notification
@notifications_bp.route("/<int:notification_id>", methods=["DELETE"])
@jwt_required()
def delete_notif(notification_id):
    user_id = get_jwt_identity()
    success = delete_notification(user_id, notification_id)
    if not success:
        return jsonify({"error": "Notification not found or unauthorized"}), 404
    return jsonify({"message": "Notification deleted"}), 200
