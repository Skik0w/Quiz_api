"""Module containing DTO models for output history."""

from datetime import datetime
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional

from quizapi.infrastructure.dto.quizdto import QuizDTO

class HistoryDTO(BaseModel):
    """A model representing DTO for history data."""
    id: int
    player_id: UUID4
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
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            HistoryDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"), # type: ignore
            player_id=record_dict.get("player_id"), # type: ignore
            quiz=QuizDTO(
                id=record_dict.get("quiz_id"), # type: ignore
                title=record_dict.get("title"), # type: ignore
                player_id=record_dict.get("player_id_2"), # type: ignore
                description=record_dict.get("description"), # type: ignore
                shared=record_dict.get("shared"), # type: ignore
                reward=record_dict.get("reward"), # type: ignore
            ),
            total_questions=record_dict.get("total_questions"), # type: ignore
            correct_answers=record_dict.get("correct_answers"), # type: ignore
            effectiveness=record_dict.get("effectiveness"), # type: ignore
            timestamp=record_dict.get("timestamp"), # type: ignore
        )
