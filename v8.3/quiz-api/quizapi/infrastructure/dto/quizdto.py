from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

from quizapi.infrastructure.dto.playerdto import PlayerDTO


class QuizDTO(BaseModel):
    id: int
    title: str
    player_id: UUID4
    description: str
    shared: bool

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "QuizDTO":
        record_dict = dict(record)
        return cls(
            id=record_dict.get("quiz_id"),  # type: ignore
            title=record_dict.get("quiz_title"), # type: ignore
            description=record_dict.get("quiz_description"), # type: ignore
            player_id=record_dict.get("player_id"),
            shared=record_dict.get("quiz_shared"), # type: ignore
        )


