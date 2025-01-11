"""Module containing DTO models for output quizzes."""

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

class QuizDTO(BaseModel):
    """A model representing DTO for quiz data."""
    id: int
    title: str
    player_id: UUID4
    description: str
    shared: bool
    reward: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "QuizDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            QuizDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("quiz_id"),  # type: ignore
            title=record_dict.get("quiz_title"), # type: ignore
            description=record_dict.get("quiz_description"), # type: ignore
            player_id=record_dict.get("player_id"), # type: ignore
            shared=record_dict.get("quiz_shared"), # type: ignore
            reward=record_dict.get("quiz_reward"), # type: ignore
        )


