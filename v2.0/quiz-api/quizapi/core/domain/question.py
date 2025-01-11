"""Module containing question-related domain models"""

from pydantic import BaseModel, ConfigDict

class QuestionIn(BaseModel):
    """Model representing question's DTO attributes."""
    question_text: str
    option_one: str
    option_two: str
    option_three: str
    option_four: str
    correct_option: str
    quiz_id: int

class Question(QuestionIn):
    """Model representing question attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")