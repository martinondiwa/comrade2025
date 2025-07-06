from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.services.media_service import save_media_metadata, get_media_by_id
from app.utils.file_storage import save_file_and_get_url, allowed_file

media_bp = Blueprint("media", __name__, url_prefix="/api/v1/media")

# Allowed media MIME types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}


# Upload media file
@media_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_media():
    user_id = get_jwt_identity()

    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    post_id = request.form.get('post_id')  # Optional for attachment to post

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        media_url, media_type = save_file_and_get_url(file, filename)

        media = save_media_metadata(
            filename=filename,
            url=media_url,
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


# Get media metadata by ID
@media_bp.route("/<int:media_id>", methods=["GET"])
@jwt_required()
def get_media(media_id):
    media = get_media_by_id(media_id)
    if not media:
        return jsonify({"error": "Media not found"}), 404

    return jsonify({
        "id": media.id,
        "url": media.url,
        "filename": media.filename,
        "media_type": media.media_type,
        "post_id": media.post_id,
        "user_id": media.user_id,
        "created_at": media.created_at.isoformat()
    }), 200
