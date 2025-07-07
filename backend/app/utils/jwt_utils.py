from flask_jwt_extended import (
    create_access_token as _create_access_token,
    decode_token,
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request
)
from datetime import timedelta
from flask import request, jsonify
from werkzeug.exceptions import Unauthorized


def create_access_token(identity: str | dict, expires_delta: timedelta = timedelta(hours=24)) -> str:
    """
    Create a new JWT access token.

    Args:
        identity (str | dict): User identity (usually user ID or email)
        expires_delta (timedelta): How long the token is valid for

    Returns:
        str: Encoded JWT token
    """
    return _create_access_token(identity=identity, expires_delta=expires_delta)


def decode_access_token(token: str) -> dict:
    """
    Decode a JWT access token manually.

    Args:
        token (str): Encoded JWT token

    Returns:
        dict: Decoded payload
    """
    try:
        return decode_token(token)
    except Exception as e:
        raise Unauthorized(f"Invalid token: {str(e)}")


def get_jwt_identity_from_request() -> str:
    """
    Extract the current user's identity from request's JWT.

    Returns:
        str: Identity from JWT (typically user_id or email)
    """
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception as e:
        raise Unauthorized("Invalid or missing JWT") from e


def get_jwt_claims() -> dict:
    """
    Retrieve all claims from the current JWT in the request.
    """
    try:
        verify_jwt_in_request()
        return get_jwt()
    except Exception as e:
        raise Unauthorized("Could not read JWT claims") from e
