"""Module containing DTO models for output tournaments."""

from typing import List

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

class TournamentDTO(BaseModel):
    """A model representing DTO for tournament data."""
    id: int
    name: str
    description: str
    quizzes_id: List[int]
    participants: List[UUID4]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "TournamentDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            TournamentDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"), # type: ignore
            name=record_dict.get("name"), # type: ignore
            description=record_dict.get("description"), # type: ignore
            participants=record_dict.get("participants"), # type: ignore
            quizzes_id=record_dict.get("quizzes_id"), # type: ignore
        )