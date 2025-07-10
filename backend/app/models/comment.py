from datetime import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from app.extensions import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)  # for threaded comments

    # Relationships
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    # Replies (self-referential relationship for nested comments)
    replies = relationship('Comment',
                           backref=backref('parent', remote_side=[id]),
                           lazy='dynamic')

    def __repr__(self):
        return f"<Comment {self.id} by User {self.user_id} on Post {self.post_id}>"
