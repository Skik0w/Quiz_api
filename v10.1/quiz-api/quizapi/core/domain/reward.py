from pydantic import BaseModel, ConfigDict, UUID4


class RewardIn(BaseModel):
    quiz_id: int

class RewardBroker(RewardIn):
    player_id: UUID4

class Reward(RewardBroker):
    id: int
    reward: str
    model_config = ConfigDict(from_attributes=True, extra="ignore")