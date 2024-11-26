"""Module containing player-related domain models."""

from typing import List
from pydantic import BaseModel, ConfigDict
from quizapi.core.domain.store import Reward

class PlayerIn(BaseModel):
    username: str
    points: int
    rewards: List[Reward]

class Player(PlayerIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")