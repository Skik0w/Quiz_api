"""Module containing quiz repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.quiz import Quiz, QuizIn

class IQuizRepository(ABC):

    @abstractmethod
    async def get_quiz_by_id(self, quiz_id: int) -> Quiz | None:
        """The abstract getting a quiz from the data storage.

        Args:
            quiz_id (int): The id of the quiz.

        Returns:
            Quiz | None: The quiz data if exists.
        """

    @abstractmethod
    async def get_all_quizzes(self) -> Iterable[Quiz]:
        """The abstract getting all quiz from the data storage.

        Returns:
            Iterable[quiz]: The collection of the all quiz.
        """

    @abstractmethod
    async def add_quiz(self, data: QuizIn) -> None:
        """The abstract adding new quiz to the data storage.

        Args:
            data (QuizIn): The attributes of the quiz.
        """

    @abstractmethod
    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn
    ) -> Quiz | None:
        """The abstract updating quiz data in the data storage.

        Args:
            quiz_id (int): The quiz id.
            data (QuizIn): The attributes of the quiz.

        Returns:
            Quiz | None: The updated quiz.
        """

    @abstractmethod
    async def delete_quiz(self, quiz_id: int) -> bool:
        """The abstract updating removing quiz from the data storage.

        Args:
            quiz_id (int): The quiz id.

        Returns:
            bool: Success of the operation.
        """