from pydantic import BaseModel, ConfigDict

class QuestionIn(BaseModel):
    text: str
    option_one: str
    option_two: str
    option_three: str
    option_four: str
    correct_answer: str
    quiz_id: int

class Question(QuestionIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")