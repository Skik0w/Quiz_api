"""Module containing quiz-related domain models"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from quizapi.core.domain.question import Question

class QuizIn(BaseModel):
    title: str
    questions: List[Question]
    player_id: int
    description: Optional[str] = None

class Quiz(QuizIn):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

