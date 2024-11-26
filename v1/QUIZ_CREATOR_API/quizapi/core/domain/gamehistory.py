"""Module containing game history-related domain models"""

from pydantic import BaseModel, ConfigDict

class GameHistoryIn(BaseModel):
    user_id: int
    quiz_id: int
    score: int
    date: str

class GameHistory(GameHistoryIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")