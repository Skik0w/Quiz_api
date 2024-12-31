from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

class ShopDTO(BaseModel):
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
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"), # type: ignore
            value=record_dict.get("value"), # type: ignore
            quiz_id=record_dict.get("quiz_id") # type: ignore
        )


