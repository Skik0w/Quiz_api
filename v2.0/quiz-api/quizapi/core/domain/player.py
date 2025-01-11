"""Module containing player-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID1

class PlayerIn(BaseModel):
    """Model representing player's DTO attributes."""

    username: str
    email: str
    password: str

class Player(PlayerIn):
    """Model representing player attributes in the database."""

    id: UUID1
    balance: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")