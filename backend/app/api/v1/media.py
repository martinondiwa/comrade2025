from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.services.media_service import save_media_metadata, get_media_by_id
from app.utils.file_storage import save_file_to_storage, allowed_file

media_bp = Blueprint("media", __name__, url_prefix="/api/v1/media")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

@media_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_media():
    user_id = get_jwt_identity()

    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    post_id = request.form.get('post_id')  # Optional

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)

        # Save the file, get saved path
        saved_path = save_file_to_storage(file, filename)

        # Detect media type by file extension
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in {'png', 'jpg', 'jpeg', 'gif'}:
            media_type = 'image'
        elif ext in {'mp4', 'mov', 'avi'}:
            media_type = 'video'
        else:
            return jsonify({"error": "Unsupported media type"}), 400

        # Create DB record via service
        media = save_media_metadata(
            filename=filename,
            url=saved_path,   # adjust this if you generate full URL elsewhere
            media_type=media_type,
            user_id=user_id,
            post_id=post_id
        )

        return jsonify({
            "message": "Upload successful",
            "media": {
                "id": media.id,
                "url": media.url,
                "type": media.media_type,
                "filename": media.filename,
                "post_id": media.post_id
            }
        }), 201

    else:
        return jsonify({"error": "Invalid file type"}), 400
