from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.infrastructure.dto.questiondto import QuestionDTO


class IQuestionService(ABC):

    @abstractmethod
    async def get_all_questions(self) -> Iterable[QuestionDTO]:
        """ """

    @abstractmethod
    async def get_question_by_id(self, question_id: int) -> QuestionDTO | None:
        """ """

    @abstractmethod
    async def add_question(self, data: QuestionIn) -> Question | None:
        """ """

    @abstractmethod
    async def update_question(
        self,
        question_id: int,
        data: QuestionIn,
    ) -> Question | None:
        """ """

    @abstractmethod
    async def delete_question(self, question_id: int) -> bool:
        """ """