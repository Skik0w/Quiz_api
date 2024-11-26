"""Module containing store-related domain models."""

from typing import Optional
from pydantic import BaseModel, ConfigDict

class RewardIn(BaseModel):
    name: str
    description: Optional[str] = None
    value: int

class Reward(RewardIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")