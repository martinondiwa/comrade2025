from app.extensions import db
from app.models.campus import Campus
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class CampusService:
    def create_campus(self, name: str, location: str, description: str = "") -> dict:
        """
        Create a new university campus.
        """
        campus = Campus(
            name=name,
            location=location,
            description=description,
            created_at=datetime.utcnow()
        )

        try:
            db.session.add(campus)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Campus with this name already exists")

        return {
            "message": "Campus created successfully",
            "campus_id": campus.id
        }

    def get_all_campuses(self) -> list:
        """
        Retrieve all campuses.
        """
        campuses = Campus.query.order_by(Campus.name.asc()).all()
        return [
            {
                "id": campus.id,
                "name": campus.name,
                "location": campus.location,
                "description": campus.description,
            }
            for campus in campuses
        ]

    def get_campus_by_id(self, campus_id: int) -> dict:
        """
        Retrieve a campus by its ID.
        """
        campus = Campus.query.get(campus_id)
        if not campus:
            raise ValueError("Campus not found")

        return {
            "id": campus.id,
            "name": campus.name,
            "location": campus.location,
            "description": campus.description,
        }

    def update_campus(self, campus_id: int, name: str = None, location: str = None, description: str = None) -> dict:
        """
        Update campus details (admin feature).
        """
        campus = Campus.query.get(campus_id)
        if not campus:
            raise ValueError("Campus not found")

        if name:
            campus.name = name
        if location:
            campus.location = location
        if description is not None:
            campus.description = description

        db.session.commit()

        return {
            "message": "Campus updated successfully",
            "campus_id": campus.id
        }

    def delete_campus(self, campus_id: int) -> dict:
        """
        Delete a campus (admin only).
        """
        campus = Campus.query.get(campus_id)
        if not campus:
            raise ValueError("Campus not found")

        db.session.delete(campus)
        db.session.commit()

        return {
            "message": "Campus deleted successfully"
        }
