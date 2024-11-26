"""Module containing quiz repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from quizapi.core.domain.quiz import QuizIn

class IQuizRepository(ABC):

    @abstractmethod
    async def get_quiz_by_id(self, quiz_id: int) -> Any | None:
        """ """

    @abstractmethod
    async def get_all_quizzes(self) -> Iterable[Any]:
        """ """

    @abstractmethod
    async def add_quiz(self, data: QuizIn) -> Any:
        """ """

    @abstractmethod
    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn
    ) -> Any | None:
        """ """

    @abstractmethod
    async def delete_quiz(self, quiz_id: int) -> bool:
        """ """