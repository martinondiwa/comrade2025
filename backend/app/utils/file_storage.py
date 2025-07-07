import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

# Allowed extensions for different media types
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi'}
ALLOWED_DOC_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Combine all into one set
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS | ALLOWED_DOC_EXTENSIONS


def allowed_file(filename: str, allowed_set: set = ALLOWED_EXTENSIONS) -> bool:
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set


def save_file_to_storage(file, subdir="uploads"):
    """
    Save a file to the designated uploads directory.

    Args:
        file (FileStorage): File from request.files
        subdir (str): Subdirectory within the UPLOAD_FOLDER (e.g., 'images', 'videos')

    Returns:
        str: Relative file path (e.g., 'uploads/images/abc123.jpg')
    """
    if file and allowed_file(file.filename):
        # Clean the filename and create a unique name
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        secure_name = secure_filename(unique_filename)

        # Create subfolder path
        upload_base = current_app.config.get("UPLOAD_FOLDER", "uploads")
        target_folder = os.path.join(upload_base, subdir)

        os.makedirs(target_folder, exist_ok=True)

        file_path = os.path.join(target_folder, secure_name)
        file.save(file_path)

        # Return the relative path to store in DB
        return os.path.relpath(file_path, start=upload_base)

    raise ValueError("File type not allowed or no file provided.")


def delete_file(relative_path, upload_root=None):
    """
    Deletes a file from storage, given a relative path.

    Args:
        relative_path (str): Path relative to UPLOAD_FOLDER
        upload_root (str): Base upload folder (optional, from config)

    Returns:
        bool: True if deleted successfully, False if not found
    """
    upload_base = upload_root or current_app.config.get("UPLOAD_FOLDER", "uploads")
    abs_path = os.path.join(upload_base, relative_path)

    if os.path.exists(abs_path):
        os.remove(abs_path)
        return True
    return False
