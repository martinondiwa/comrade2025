from flask import request
from math import ceil


def paginate_query(query, page=None, per_page=None, max_per_page=100, item_serializer=None):
    """
    Paginate a SQLAlchemy query and return structured data with metadata.

    Args:
        query (db.Query): SQLAlchemy query object.
        page (int): Page number (optional, default: from request args).
        per_page (int): Items per page (optional, default: from request args).
        max_per_page (int): Upper limit on per_page to prevent abuse.
        item_serializer (callable): Function to convert model instance to dict. Defaults to `.to_dict()`.

    Returns:
        dict: {
            "items": [...],
            "pagination": {
                "total": int,
                "page": int,
                "per_page": int,
                "pages": int,
                "has_next": bool,
                "has_prev": bool
            }
        }

    Raises:
        ValueError: For invalid page/per_page input.
    """
    try:
        page = page or int(request.args.get("page", 1))
        per_page = per_page or int(request.args.get("per_page", 20))

        if page < 1 or per_page < 1:
            raise ValueError("page and per_page must be positive integers")

        per_page = min(per_page, max_per_page)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        serializer = item_serializer or (lambda item: item.to_dict())

        return {
            "items": [serializer(item) for item in pagination.items],
            "pagination": {
                "total": pagination.total,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }

    except Exception as e:
        raise ValueError(f"Pagination failed: {str(e)}")
