from datetime import datetime
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict
from typing import Optional

from quizapi.infrastructure.dto.playerdto import PlayerDTO
from quizapi.infrastructure.dto.quizdto import QuizDTO


class HistoryDTO(BaseModel):
    id: int
    player: PlayerDTO
    quiz: QuizDTO
    total_questions: int
    correct_answers: Optional[int]
    effectiveness: Optional[float]
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "HistoryDTO":
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),
            player=PlayerDTO(
                id=record_dict.get("player_id1"),
                username=record_dict.get("player_username1"),
            ),
            quiz=QuizDTO(
                id=record_dict.get("quiz_id"),
                title=record_dict.get("title"),
                player=PlayerDTO(
                    id=record_dict.get("player_id2"),
                    username=record_dict.get("player_username2"),
                ),
                description=record_dict.get("description"),
                shared=record_dict.get("shared"),
            ),
            total_questions=record_dict.get("total_questions"),
            correct_answers=record_dict.get("correct_answers"),
            effectiveness=record_dict.get("effectiveness"),
            timestamp=record_dict.get("timestamp"),
        )
