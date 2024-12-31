from pydantic import BaseModel, ConfigDict, UUID4
from typing import List

class TournamentIn(BaseModel):
    name: str
    description: str
    quizzes_id: List[int]

class Tournament(TournamentIn):
    id: int
    participants: List[UUID4]
    model_config = ConfigDict(from_attributes=True, extra="ignore")