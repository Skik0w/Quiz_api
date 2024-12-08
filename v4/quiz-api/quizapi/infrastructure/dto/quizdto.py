from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

class QuizDTO(BaseModel):
    id: int
    title: str
    #question_id: int
    player_id: int
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "QuizDTO":

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"), # type ignore
            title=record_dict.get("title"), # type ignore
            #question_id=record_dict.get("question_id"),
            player_id=record_dict.get("player_id"), # type: ignore
            description=record_dict.get("description"), # type: ignore
        )
