"""Module containing quiz service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.infrastructure.dto.quizdto import QuizDTO


class IQuizService(ABC):
    """An abstract class representing protocol of quiz service."""

    @abstractmethod
    async def get_all_quizzes(self) -> Iterable[QuizDTO]:
        """The abstract getting all quizzes from the repository.

        Returns:
            Iterable[QuizDTO]: The collection of all quizzes.
        """

    @abstractmethod
    async def get_quiz_by_id(self, quiz_id: int) -> QuizDTO | None:
        """The abstract getting a quiz by ID from the repository.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            QuizDTO | None: The quiz data if exists.
        """

    @abstractmethod
    async def add_quiz(self, data: QuizIn) -> Quiz | None:
        """The abstract adding a new quiz to the repository.

        Args:
            data (QuizIn): The attributes of the quiz.

        Returns:
            Quiz | None: The newly created quiz if successful.
        """

    @abstractmethod
    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn
    ) -> Quiz | None:
        """The abstract updating a quiz in the repository.

        Args:
            quiz_id (int): The ID of the quiz.
            data (QuizIn): The updated attributes of the quiz.

        Returns:
            Quiz | None: The updated quiz if successful.
        """

    @abstractmethod
    async def delete_quiz(self, quiz_id: int) -> bool:
        """The abstract removing a quiz from the repository.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            bool: Success of the operation.
        """

    async def share_quiz(self, quiz_id: int) -> Quiz | None:
        """The abstract sharing a quiz by updating its shared status in the repository.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Quiz | None: The updated quiz if successful.
        """