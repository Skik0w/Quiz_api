"""Module containing tournament-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4
from typing import List

class TournamentIn(BaseModel):
    """Model representing tournament's DTO attributes."""
    name: str
    description: str
    quizzes_id: List[int]

class Tournament(TournamentIn):
    """Model representing tournament attributes in the database."""
    id: int
    participants: List[UUID4]
    model_config = ConfigDict(from_attributes=True, extra="ignore")