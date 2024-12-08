from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

class PlayerDTO(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
