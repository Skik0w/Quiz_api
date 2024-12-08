from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

class QuestionDTO(BaseModel):
    id: int
    text: str
    option_one: str
    option_two: str
    option_three: str
    option_four: str
    correct_answer: str
    question_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )