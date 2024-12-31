from pydantic import BaseModel, ConfigDict, UUID4
from typing import List, Optional

class TournamentIn(BaseModel):
    name: str
    description: str
    quizzes_id: List[int]

class TournamentBroker(TournamentIn):
    players_id: Optional[List[UUID4]]

class Tournament(TournamentBroker):
    id: int
    results: Optional[dict]

    model_config = ConfigDict(from_attributes=True, extra="ignore")