from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.event_service import EventService
from app.services.user_service import get_user_by_id

events_bp = Blueprint("events", __name__, url_prefix="/api/v1/events")

# Instantiate the service once
event_service = EventService()


# Get all events
@events_bp.route("/", methods=["GET"])
# @jwt_required()
def list_events():
    events = event_service.get_all_events()
    return jsonify([
        {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "location": e.location,
            "event_date": e.event_date.isoformat(),
            "creator_id": e.user_id,
            "created_at": e.created_at.isoformat()
        }
        for e in events
    ]), 200


# Get a specific event
@events_bp.route("/<int:event_id>", methods=["GET"])
# @jwt_required()
def get_event(event_id):
    event = event_service.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    return jsonify({
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "location": event.location,
        "event_date": event.event_date.isoformat(),
        "creator_id": event.user_id,
        "created_at": event.created_at.isoformat()
    }), 200


# Create a new event
@events_bp.route("/", methods=["POST"])
# @jwt_required()
def create_new_event():
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    location = data.get("location")
    event_date = data.get("event_date")

    if not all([title, location, event_date]):
        return jsonify({"error": "Title, location, and event date are required"}), 400

    event = event_service.create_event(user_id, title, description, location, event_date)
    return jsonify({
        "message": "Event created successfully",
        "event": {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "location": event.location,
            "event_date": event.event_date.isoformat(),
            "creator_id": event.user_id
        }
    }), 201


# Update an event (creator or admin)
@events_bp.route("/<int:event_id>", methods=["PUT"])
# @jwt_required()
def update_existing_event(event_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    event = event_service.get_event_by_id(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    if event.user_id != user_id and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    updated_event = event_service.update_event(
        event_id,
        title=data.get("title", event.title),
        description=data.get("description", event.description),
        location=data.get("location", event.location),
        event_date=data.get("event_date", event.event_date.isoformat())
    )

    return jsonify({
        "message": "Event updated successfully",
        "event": {
            "id": updated_event.id,
            "title": updated_event.title,
            "location": updated_event.location,
            "event_date": updated_event.event_date.isoformat()
        }
    }), 200


# Delete event (creator or admin)
@events_bp.route("/<int:event_id>", methods=["DELETE"])
# @jwt_required()
def delete_event_route(event_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    event = event_service.get_event_by_id(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    if event.user_id != user_id and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    event_service.delete_event(event_id)
    return jsonify({"message": f"Event {event_id} deleted successfully"}), 200


# ===============================
# TEMPORARY: Add sample events
# ===============================
@events_bp.route("/seed", methods=["POST"])
def seed_events():
    default_user_id = 1  # Replace with a valid user ID if needed

    sample_events = [
        {
            "title": "Campus Coding Marathon",
            "description": "A 24-hour hackathon for university students.",
            "location": "ICT Hall A",
            "event_date": "2025-08-01T10:00:00"
        },
        {
            "title": "Art & Culture Exhibition",
            "description": "Showcasing local artists, food, and music.",
            "location": "Nairobi Gallery",
            "event_date": "2025-08-15T14:00:00"
        },
        {
            "title": "Tech Networking Night",
            "description": "Connect with startup founders and software engineers.",
            "location": "iHub, Nairobi",
            "event_date": "2025-08-20T18:00:00"
        },
        {
            "title": "Climate Action Workshop",
            "description": "Youth-led solutions for sustainable agriculture.",
            "location": "UN Avenue Conference Room",
            "event_date": "2025-09-05T09:00:00"
        }
    ]

    created_events = []
    for event in sample_events:
        created = event_service.create_event(
            default_user_id,
            event["title"],
            event["description"],
            event["location"],
            event["event_date"]
        )
        created_events.append({
            "id": created.id,
            "title": created.title,
            "description": created.description,
            "location": created.location,
            "event_date": created.event_date.isoformat()
        })

    return jsonify({
        "message": f"{len(created_events)} events seeded successfully",
        "events": created_events
    }), 201
