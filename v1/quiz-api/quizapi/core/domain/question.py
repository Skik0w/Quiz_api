"""Module containing question-related domain models"""

from typing import List

from pydantic import BaseModel, ConfigDict

class QuestionIn(BaseModel):
    text: str
    options: List[str]
    correct_answer: int

class Question(QuestionIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")