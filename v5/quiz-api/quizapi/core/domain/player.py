from pydantic import BaseModel, ConfigDict

class PlayerIn(BaseModel):
    username: str

class Player(PlayerIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")