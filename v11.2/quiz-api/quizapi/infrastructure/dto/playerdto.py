from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

class PlayerDTO(BaseModel):
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
        record_dict = dict(record)
        return cls(
            id=record_dict.get("quiz_id"),  # type: ignore
            username=record_dict.get("username"),
            email=record_dict.get("email"),
            balance=record_dict.get("balance") or 0,
        )