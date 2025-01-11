"""A module containing helper functions for token generation."""

from datetime import datetime, timedelta, timezone

from jose import jwt
from pydantic import UUID4

from quizapi.infrastructure.utils.consts import (
    EXPIRATION_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)


def generate_player_token(player_uuid: UUID4) -> dict:
    """A function returning JWT token for user.

    Args:
        player_uuid (UUID4): The UUID of the user.

    Returns:
        dict: The token details.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    jwt_data = {"sub": str(player_uuid), "exp": expire, "type": "confirmation"}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)

    return {"player_token": encoded_jwt, "expires": expire}