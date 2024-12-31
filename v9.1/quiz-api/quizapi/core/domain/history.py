from datetime import datetime
from pydantic import BaseModel, ConfigDict, UUID4

class HistoryIn(BaseModel):
    quiz_id: int
    correct_answers: int
    timestamp: datetime

class HistoryBroker(HistoryIn):
    player_id: UUID4

class History(HistoryBroker):
    id: int
    total_questions: int
    effectiveness: float

    model_config = ConfigDict(from_attributes=True, extra="ignore")