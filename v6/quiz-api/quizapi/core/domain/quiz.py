from pydantic import BaseModel, ConfigDict

class QuizIn(BaseModel):
    title: str
    player_id: int
    description: str

class Quiz(QuizIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")