from datetime import datetime
from app.extensions import db
from app.models.event import Event
from app.models.user import User
from sqlalchemy.exc import IntegrityError


class EventService:
    def create_event(self, title: str, description: str, location: str, start_time: datetime, end_time: datetime, created_by: int, campus_id: int = None, group_id: int = None) -> dict:
        """
        Create a new event.
        """
        creator = User.query.get(created_by)
        if not creator:
            raise ValueError("User not found")

        event = Event(
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            created_by=created_by,
            campus_id=campus_id,
            group_id=group_id,
            created_at=datetime.utcnow()
        )

        db.session.add(event)
        db.session.commit()

        return {
            "message": "Event created successfully",
            "event_id": event.id
        }

    def get_all_events(self, campus_id=None, group_id=None) -> list:
        """
        Retrieve events optionally filtered by campus or group.
        """
        query = Event.query

        if campus_id:
            query = query.filter_by(campus_id=campus_id)
        if group_id:
            query = query.filter_by(group_id=group_id)

        events = query.order_by(Event.start_time.asc()).all()

        return [
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "location": event.location,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "campus_id": event.campus_id,
                "group_id": event.group_id,
                "created_by": event.created_by
            }
            for event in events
        ]

    def get_event_by_id(self, event_id: int) -> dict:
        """
        Get details of a specific event.
        """
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found")

        return {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "location": event.location,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat(),
            "campus_id": event.campus_id,
            "group_id": event.group_id,
            "created_by": event.created_by
        }

    def update_event(self, event_id: int, user_id: int, **kwargs) -> dict:
        """
        Update event details — only the creator can update.
        """
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found")
        if event.created_by != user_id:
            raise PermissionError("Only the event creator can update this event.")

        for key in ["title", "description", "location", "start_time", "end_time"]:
            if key in kwargs:
                setattr(event, key, kwargs[key])

        db.session.commit()

        return {
            "message": "Event updated successfully",
            "event_id": event.id
        }

    def delete_event(self, event_id: int, user_id: int) -> dict:
        """
        Delete an event — only the creator can delete.
        """
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found")
        if event.created_by != user_id:
            raise PermissionError("Only the event creator can delete this event.")

        db.session.delete(event)
        db.session.commit()

        return {
            "message": "Event deleted successfully"
        }
