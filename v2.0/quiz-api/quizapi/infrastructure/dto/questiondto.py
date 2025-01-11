"""Module containing DTO models for output questions."""

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from quizapi.infrastructure.dto.quizdto import QuizDTO

class QuestionDTO(BaseModel):
    """A model representing DTO for question data."""
    id: int
    question_text: str
    option_one: str
    option_two: str
    option_three: str
    option_four: str
    correct_option: str
    quiz: QuizDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "QuestionDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            QuestionDTO: The final DTO instance.
        """
        record_dict = dict(record)
        return cls(
            id=record_dict.get("id"), # type ignore
            question_text=record_dict.get("question_text"), # type: ignore
            option_one=record_dict.get("option_one"), # type: ignore
            option_two=record_dict.get("option_two"), # type: ignore
            option_three=record_dict.get("option_three"), # type: ignore
            option_four=record_dict.get("option_four"), # type: ignore
            correct_option=record_dict.get("correct_option"), # type: ignore
            quiz=QuizDTO(
                id=record_dict.get("quiz_id"), # type: ignore
                title=record_dict.get("title"), # type: ignore
                player_id=record_dict.get("player_id"), # type: ignore
                description=record_dict.get("description"), # type: ignore
                shared=record_dict.get("shared"), # type: ignore
                reward=record_dict.get("reward") # type: ignore
            )
        )