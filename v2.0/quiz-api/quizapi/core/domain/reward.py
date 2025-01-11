"""Module containing reward-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4

class RewardIn(BaseModel):
    """Model representing reward's DTO attributes."""
    quiz_id: int

class RewardBroker(RewardIn):
    """A broker class including user in the model."""
    player_id: UUID4

class Reward(RewardBroker):
    """Model representing reward attributes in the database."""
    id: int
    reward: str
    value: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")