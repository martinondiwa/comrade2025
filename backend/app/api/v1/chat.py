from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.chat_service import (
    send_message,
    get_conversation_history,
    get_recent_conversations
)
from app.services.user_service import get_user_by_id

chat_bp = Blueprint("chat", __name__, url_prefix="/api/v1/chat")


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

    # Optional: Block messaging self
    if user_id == recipient_id:
        return jsonify({"error": "You cannot message yourself"}), 400

    recipient = get_user_by_id(recipient_id)
    if not recipient:
        return jsonify({"error": "Recipient does not exist"}), 404

    message = send_message(sender_id=user_id, recipient_id=recipient_id, message=message_text)

    return jsonify({
        "message": "Message sent successfully",
        "chat": {
            "id": message.id,
            "sender_id": message.sender_id,
            "recipient_id": message.recipient_id,
            "text": message.message,
            "timestamp": message.timestamp.isoformat()
        }
    }), 201


# Get conversation between current user and another user
@chat_bp.route("/conversation/<int:recipient_id>", methods=["GET"])
@jwt_required()
def get_conversation(recipient_id):
    user_id = get_jwt_identity()
    messages = get_conversation_history(user_id, recipient_id)

    return jsonify([
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "recipient_id": m.recipient_id,
            "message": m.message,
            "timestamp": m.timestamp.isoformat()
        }
        for m in messages
    ]), 200


# Get recent conversations (last messages from each chat)
@chat_bp.route("/recent", methods=["GET"])
@jwt_required()
def get_recent_chats():
    user_id = get_jwt_identity()
    conversations = get_recent_conversations(user_id)

    return jsonify([
        {
            "with_user_id": convo["with_user_id"],
            "with_user_name": convo["with_user_name"],
            "last_message": convo["last_message"],
            "timestamp": convo["timestamp"].isoformat()
        }
        for convo in conversations
    ]), 200
