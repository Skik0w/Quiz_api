from pydantic import BaseModel, ConfigDict, UUID1

class PlayerIn(BaseModel):
    username: str
    email: str
    password: str

class Player(PlayerIn):
    id: UUID1
    balance: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")