"""
Utils package initializer.

This package contains utility functions and classes used throughout the Comrade backend:
- JWT handling
- File and media storage
- Pagination
- Media optimization (images/videos)
"""

# Expose key utilities at package level
from .jwt_utils import (
    create_access_token,
    decode_access_token,
    get_jwt_identity_from_request
)

from .file_storage import (
    save_file_to_storage,
    allowed_file,
    delete_file
)

from .pagination import paginate_query

from .image_optimizer import optimize_image
from .video_optimizer import process_video_compression

__all__ = [
    "create_access_token",
    "decode_access_token",
    "get_jwt_identity_from_request",
    "save_file_to_storage",
    "allowed_file",
    "delete_file",
    "paginate_query",
    "optimize_image",
    "process_video_compression"
]
