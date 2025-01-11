"""Module containing DTO models for output tokens."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TokenDTO(BaseModel):
    """A model representing DTO for authentication tokens."""
    token_type: str
    player_token: str
    expires: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )