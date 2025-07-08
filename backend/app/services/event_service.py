from datetime import datetime
from app.extensions import db
from app.models.event import Event
from app.models.user import User
from sqlalchemy.exc import IntegrityError


class EventService:
    def create_event(self, title: str, description: str, location: str, start_time: datetime, end_time: datetime, created_by: int, campus_id: int = None, group_id: int = None) -> Event:
        """
        Create a new event and return the Event object.
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

        return event  # Return ORM instance

    def get_all_events(self, campus_id=None, group_id=None) -> list:
        """
        Retrieve events optionally filtered by campus or group, returning list of ORM Event objects.
        """
        query = Event.query

        if campus_id:
            query = query.filter_by(campus_id=campus_id)
        if group_id:
            query = query.filter_by(group_id=group_id)

        events = query.order_by(Event.start_time.asc()).all()
        return events  # Return list of ORM instances

    def get_event_by_id(self, event_id: int) -> Event:
        """
        Get Event object by id.
        """
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found")
        return event  # Return ORM instance

    def update_event(self, event_id: int, user_id: int, **kwargs) -> Event:
        """
        Update event details — only the creator can update. Returns updated Event object.
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
        return event  # Return updated ORM instance

    def delete_event(self, event_id: int, user_id: int) -> None:
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
