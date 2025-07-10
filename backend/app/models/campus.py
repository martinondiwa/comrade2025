from app.extensions import db
from datetime import datetime


class Campus(db.Model):
    __tablename__ = 'campuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    university = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Updated relationship to match User model using back_populates
    users = db.relationship('User', back_populates='campus', lazy=True)
    posts = db.relationship('Post', back_populates='campus', lazy=True)
    events = db.relationship('Event', back_populates='campus', lazy=True)

    def __repr__(self):
        return f"<Campus {self.name} - {self.university}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "university": self.university,
            "location": self.location,
            "created_at": self.created_at.isoformat()
        }
