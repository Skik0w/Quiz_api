"""Module containing DTO models for output players."""

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

class PlayerDTO(BaseModel):
    """A model representing DTO for player data."""
    id: UUID4
    username: str
    email: str
    balance: int = 0


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record: Record) -> "PlayerDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            PlayerDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("quiz_id"),  # type: ignore
            username=record_dict.get("username"), # type: ignore
            email=record_dict.get("email"), # type: ignore
            balance=record_dict.get("balance") or 0, # type: ignore
        )