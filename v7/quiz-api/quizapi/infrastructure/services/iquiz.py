from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.infrastructure.dto.quizdto import QuizDTO


class IQuizService(ABC):

    @abstractmethod
    async def get_all_quizzes(self) -> Iterable[QuizDTO]:
        """ """

    @abstractmethod
    async def get_quiz_by_id(self, quiz_id: int) -> QuizDTO | None:
        """ """

    @abstractmethod
    async def add_quiz(self, data: QuizIn) -> Quiz | None:
        """ """

    @abstractmethod
    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn
    ) -> Quiz | None:
        """ """

    @abstractmethod
    async def delete_quiz(self, quiz_id: int) -> bool:
        """ """

    async def share_quiz(self, quiz_id: int) -> Quiz | None:
        """ """