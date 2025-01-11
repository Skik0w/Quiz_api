"""Module containing history-related domain models"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, UUID4

class HistoryIn(BaseModel):
    """Model representing history's DTO attributes."""
    quiz_id: int
    correct_answers: int
    timestamp: datetime

class HistoryBroker(HistoryIn):
    """A broker class including user in the model."""
    player_id: UUID4

class History(HistoryBroker):
    """Model representing history attributes in the database."""
    id: int
    total_questions: int
    effectiveness: float

    model_config = ConfigDict(from_attributes=True, extra="ignore")