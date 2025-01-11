"""Module containing DTO models for output shop items."""

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

class ShopDTO(BaseModel):
    """A model representing DTO for shop item data."""
    id: int
    name: str
    value: int
    quiz_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ShopDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ShopDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"), # type: ignore
            name=record_dict.get("name"), # type: ignore
            value=record_dict.get("value"), # type: ignore
            quiz_id=record_dict.get("quiz_id") # type: ignore
        )


