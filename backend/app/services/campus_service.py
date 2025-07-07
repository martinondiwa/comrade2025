from app import db
from app.models import Campus


class CampusService:
    @staticmethod
    def get_all_campuses():
        return Campus.query.all()

    @staticmethod
    def get_campus_by_id(campus_id):
        return Campus.query.get(campus_id)

    @staticmethod
    def create_campus(name, location, description=None):
        new_campus = Campus(name=name, location=location, description=description)
        db.session.add(new_campus)
        db.session.commit()
        return new_campus

    @staticmethod
    def update_campus(campus_id, name, location, description):
        campus = Campus.query.get(campus_id)
        if not campus:
            return None
        campus.name = name
        campus.location = location
        campus.description = description
        db.session.commit()
        return campus

    @staticmethod
    def delete_campus(campus_id):
        campus = Campus.query.get(campus_id)
        if campus:
            db.session.delete(campus)
            db.session.commit()
