from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from quizapi.infrastructure.dto.playerdto import PlayerDTO


class QuizDTO(BaseModel):
    id: int
    title: str
    player: PlayerDTO
    description: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "QuizDTO":
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"), # type: ignore
            title=record_dict.get("title"), # type: ignore
            player=PlayerDTO(
                id=record_dict.get("id_1"), # type: ignore
                username=record_dict.get("username"), # type: ignore
            ),
            description=record_dict.get("description"), # type: ignore
        )


