from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

class RewardDTO(BaseModel):
    id: int
    quiz_id: int
    player_id: UUID4
    reward: str
    value: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "RewardDTO":
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"),  # type: ignore
            quiz_id=record_dict.get("quiz_id"), # type: ignore
            player_id=record_dict.get("player_id"), # type: ignore
            reward=record_dict.get("reward"), # type: ignore
            value=record_dict.get("value") # type: ignore
        )


