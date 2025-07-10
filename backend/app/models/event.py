from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from app.extensions import db

# Association table for attendees (many-to-many)
event_attendees = Table(
    'event_attendees',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    campus_id = Column(Integer, ForeignKey('campuses.id'), nullable=True)

    # Relationships
    creator = db.relationship('User', back_populates='created_events')
    campus = db.relationship('Campus', back_populates='events')

    attendees = relationship('User',
                             secondary=event_attendees,
                             backref=backref('events_attending', lazy='dynamic'))

    def __repr__(self):
        return f"<Event {self.title} by User {self.creator_id}>"
