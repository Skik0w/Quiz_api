"""Module containing quiz repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable
from quizapi.core.domain.quiz import QuizIn

class IQuizRepository(ABC):
    """An abstract class representing protocol of quiz repository."""

    @abstractmethod
    async def get_all_quizzes(self) -> Iterable[Any]:
        """The abstract getting all quizzes from the data storage.

        Returns:
            Iterable[Any]: The collection of all quizzes.
        """
    @abstractmethod
    async def get_quiz_by_id(self, quiz_id: int) -> Any | None:
        """The abstract getting a quiz by ID from the data storage.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Any | None: The quiz data if exists.
        """

    @abstractmethod
    async def add_quiz(self, data: QuizIn) -> Any | None:
        """The abstract adding a new quiz to the data storage.

        Args:
            data (QuizIn): The attributes of the quiz.

        Returns:
            Any | None: The newly created quiz.
        """

    @abstractmethod
    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn
    ) -> Any | None:
        """The abstract updating quiz data in the data storage.

        Args:
            quiz_id (int): The ID of the quiz.
            data (QuizIn): The updated attributes of the quiz.

        Returns:
            Any | None: The updated quiz.
        """

    @abstractmethod
    async def delete_quiz(self, quiz_id: int) -> bool:
        """The abstract removing a quiz from the data storage.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def share_quiz(self, quiz_id: int) -> Any | None:
        """The abstract sharing a quiz in the data storage.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Any | None: The shared quiz data if successful.
        """

    @abstractmethod
    async def get_quiz_by_reward(self, reward: str) -> Any | None:
        """The abstract getting a quiz by reward from the data storage.

        Args:
            reward (str): The reward name associated with the quiz.

        Returns:
            Any | None: The quiz data if exists.
        """
