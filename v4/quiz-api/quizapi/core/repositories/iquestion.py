"""Module containing question repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from quizapi.core.domain.question import QuestionIn


class IQuestionRepository(ABC):

    @abstractmethod
    async def get_question_by_id(self, question_id: int) -> Any | None:
        """ """

    @abstractmethod
    async def get_all_questions(self) -> Iterable[Any]:
        """ """

    @abstractmethod
    async def add_question(self, data: QuestionIn) -> Any | None:
        """ """

    @abstractmethod
    async def update_question(
        self,
        question_id: int,
        data: QuestionIn,
    ) -> Any | None:
        """ """

    @abstractmethod
    async def delete_question(self, question_id: int) -> bool:
        """ """