from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

class PlayerDTO(BaseModel):
    id: UUID4
    username: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )