from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.quiz import Quiz, QuizIn

class IQuizService(ABC):

    @abstractmethod
    async def get_quiz_by_id(self, quiz_id: int) -> Quiz | None:
        """ """

    @abstractmethod
    async def get_all_quizzes(self) -> Iterable[Quiz]:
        """ """

    @abstractmethod
    async def add_quiz(self, data: QuizIn) -> None:
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