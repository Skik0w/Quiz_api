from datetime import datetime
from pydantic import BaseModel, ConfigDict

class HistoryIn(BaseModel):
    player_id: int
    quiz_id: int
    correct_answers: int
    total_questions: int
    effectiveness: float
    timestamp: datetime

class History(HistoryIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")