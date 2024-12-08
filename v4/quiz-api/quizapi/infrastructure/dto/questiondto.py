from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from quizapi.infrastructure.dto.playerdto import PlayerDTO
from quizapi.infrastructure.dto.quizdto import QuizDTO


class QuestionDTO(BaseModel):
    id: int
    text: str
    option_one: str
    option_two: str
    option_three: str
    option_four: str
    correct_answer: str
    quiz: QuizDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "QuestionDTO":

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"), # type ignore
            text=record_dict.get("text"),
            option_one=record_dict.get("option_one"),
            option_two=record_dict.get("option_two"),
            option_three=record_dict.get("option_three"),
            option_four=record_dict.get("option_four"),
            correct_answer=record_dict.get("correct_answer"),
            quiz=QuizDTO(
                id=record_dict.get("id_1"), # type: ignore
                title=record_dict.get("title_1"), # type: ignore
                player=PlayerDTO(
                    id=record_dict.get("id_2"),  # type: ignore
                    username=record_dict.get("username"),  # type: ignore
                ),
                description=record_dict.get("description"), # type: ignore
            )
        )