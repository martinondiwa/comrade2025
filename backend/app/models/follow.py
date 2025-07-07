from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from app.extensions import db

class Follow(db.Model):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    follower = relationship('User', foreign_keys=[follower_id], backref=backref('following', lazy='dynamic'))
    followed = relationship('User', foreign_keys=[followed_id], backref=backref('followers', lazy='dynamic'))

    # Prevent duplicate follows
    __table_args__ = (UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),)

    def __repr__(self):
        return f"<Follow {self.follower_id} -> {self.followed_id}>"
