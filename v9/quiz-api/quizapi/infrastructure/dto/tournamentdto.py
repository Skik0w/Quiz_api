from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional, Dict, List

class TournamentDTO(BaseModel):
    id: int
    name: str
    description: str
    quizzes: List[int]
    players: Optional[List[UUID4]] = None
    results: Optional[Dict[str, int]] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "TournamentDTO":
        record_dict = dict(record)
        return cls(
            id=record_dict.get("tournament_id"),  # type: ignore
            name=record_dict.get("tournament_name"), # type: ignore
            description=record_dict.get("tournament_description"), # type: ignore
            quizzes=record_dict.get("tournament_quizzes"),
            players=record_dict.get("tournament_players"),
            results=record_dict.get("tournament_results")
        )


