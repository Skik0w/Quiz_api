from pydantic import BaseModel, ConfigDict, UUID4


class QuizIn(BaseModel):
    title: str
    description: str
    shared: bool
    reward: str

class QuizBroker(QuizIn):
    player_id: UUID4

class Quiz(QuizBroker):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")