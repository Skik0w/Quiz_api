"""Module containing quiz-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4

class QuizIn(BaseModel):
    """Model representing quiz's DTO attributes."""
    title: str
    description: str
    shared: bool
    reward: str

class QuizBroker(QuizIn):
    """A broker class including user in the model."""
    player_id: UUID4

class Quiz(QuizBroker):
    """Model representing quiz attributes in the database."""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")