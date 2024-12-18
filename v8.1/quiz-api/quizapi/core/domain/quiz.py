from pydantic import BaseModel, ConfigDict, UUID4


class QuizIn(BaseModel):
    title: str
    player_username: str
    description: str
    shared: bool

class QuizBroker(QuizIn):
    player_id: UUID4

class Quiz(QuizBroker):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")