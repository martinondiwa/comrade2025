from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.chat_service import ChatService
from app.services.user_service import get_user_by_id

chat_bp = Blueprint("chat", __name__, url_prefix="/api/v1/chat")

# Instantiate the service once
chat_service = ChatService()

# Send a message (text only for now)
@chat_bp.route("/send", methods=["POST"])
@jwt_required()
def send_chat_message():
    user_id = get_jwt_identity()
    data = request.get_json()

    recipient_id = data.get("recipient_id")
    message_text = data.get("message")

    if not recipient_id or not message_text:
        return jsonify({"error": "recipient_id and message are required"}), 400

    if user_id == recipient_id:
        return jsonify({"error": "You cannot message yourself"}), 400

    recipient = get_user_by_id(recipient_id)
    if not recipient:
        return jsonify({"error": "Recipient does not exist"}), 404

    # Call method on service instance
    message_info = chat_service.send_message(sender_id=user_id, recipient_id=recipient_id, content=message_text)

    return jsonify({
        "message": "Message sent successfully",
        "chat": message_info
    }), 201

# Get conversation between current user and another user
@chat_bp.route("/conversation/<int:recipient_id>", methods=["GET"])
@jwt_required()
def get_conversation(recipient_id):
    user_id = get_jwt_identity()
    messages = chat_service.get_conversation(user1_id=user_id, user2_id=recipient_id)

    return jsonify([
        {
            "id": m["id"],
            "sender_id": m["sender_id"],
            "recipient_id": m["recipient_id"],
            "content": m["content"],
            "timestamp": m["timestamp"],
            "is_read": m["is_read"]
        }
        for m in messages
    ]), 200

# Get recent conversations (last messages from each chat) - implement as needed
@chat_bp.route("/recent", methods=["GET"])
@jwt_required()
def get_recent_chats():
    user_id = get_jwt_identity()
    # If you have implemented a method `get_recent_conversations` in ChatService, call it here.
    # For now, just return empty list or implement accordingly.
    conversations = []  # or chat_service.get_recent_conversations(user_id)
    return jsonify(conversations), 200
