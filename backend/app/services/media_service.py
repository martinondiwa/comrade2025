import os
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.media import Media
from app.utils.file_storage import save_file_to_storage, delete_file
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mkv'}

class MediaService:

    def allowed_file(self, filename: str) -> bool:
        """
        Check if the file has an allowed extension.
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_media(self, user_id: int, file_storage, media_type: str = None) -> dict:
        """
        Save media file to storage and create DB record.
        
        Args:
            user_id (int): uploader user ID
            file_storage: werkzeug FileStorage object
            media_type (str): 'image' or 'video' (optional)
        Returns:
            dict: info about saved media
        """
        filename = secure_filename(file_storage.filename)
        if not filename:
            raise ValueError("Invalid file name.")

        if not self.allowed_file(filename):
            raise ValueError(f"Unsupported file extension. Allowed: {ALLOWED_EXTENSIONS}")

        # Auto-detect media type by extension if not provided
        ext = filename.rsplit('.', 1)[1].lower()
        if not media_type:
            if ext in {'png', 'jpg', 'jpeg', 'gif'}:
                media_type = 'image'
            elif ext in {'mp4', 'mov', 'avi', 'mkv'}:
                media_type = 'video'
            else:
                raise ValueError("Could not detect media type.")

        # Save file using utility (handles directory, unique naming, etc.)
        saved_path = save_file(file_storage, media_type)

        # Create DB record
        media = Media(
            user_id=user_id,
            filename=filename,
            media_type=media_type,
            filepath=saved_path,
            uploaded_at=datetime.utcnow()
        )

        db.session.add(media)
        db.session.commit()

        return {
            "media_id": media.id,
            "filename": media.filename,
            "media_type": media.media_type,
            "filepath": media.filepath,
            "uploaded_at": media.uploaded_at.isoformat()
        }

    def get_media(self, media_id: int) -> dict:
        """
        Retrieve media metadata by ID.
        """
        media = Media.query.get(media_id)
        if not media:
            raise ValueError("Media not found.")

        return {
            "media_id": media.id,
            "filename": media.filename,
            "media_type": media.media_type,
            "filepath": media.filepath,
            "uploaded_at": media.uploaded_at.isoformat(),
            "user_id": media.user_id
        }

    def delete_media(self, media_id: int, user_id: int) -> dict:
        """
        Delete media file and DB record if owned by user.
        """
        media = Media.query.get(media_id)
        if not media:
            raise ValueError("Media not found.")
        if media.user_id != user_id:
            raise PermissionError("User does not have permission to delete this media.")

        # Delete physical file
        delete_file(media.filepath)

        # Delete DB record
        db.session.delete(media)
        db.session.commit()

        return {
            "message": "Media deleted successfully",
            "media_id": media_id
        }
