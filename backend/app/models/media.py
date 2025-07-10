from app.extensions import db
from datetime import datetime


class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)  # e.g., "image", "video"
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)  # Optional: media can be standalone or linked to posts
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    uploader = db.relationship("User", back_populates="media_files")
    post = db.relationship("Post", back_populates="media")

    def __repr__(self):
        return f"<Media {self.filename} ({self.media_type})>"

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "url": self.url,
            "media_type": self.media_type,
            "uploader_id": self.uploader_id,
            "post_id": self.post_id,
            "uploaded_at": self.uploaded_at.isoformat(),
        }
