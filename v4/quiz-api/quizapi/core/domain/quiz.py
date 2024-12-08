"""Module containing quiz-related domain models"""

from typing import Optional
from pydantic import BaseModel, ConfigDict
from quizapi.core.domain.question import Question

class QuizIn(BaseModel):
    title: str
    #question_id: int  #questions: list[Question]
    player_id: int
    description: str

class Quiz(QuizIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")