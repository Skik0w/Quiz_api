"""Module containing question repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable

from quizapi.core.domain.question import QuestionIn


class IQuestionRepository(ABC):
    """An abstract class representing protocol of question repository."""

    @abstractmethod
    async def get_all_questions(self) -> Iterable[Any]:
        """The abstract getting all questions from the data storage.

        Returns:
            Iterable[Any]: The collection of all questions.
        """

    @abstractmethod
    async def get_question_by_id(self, question_id: int) -> Any | None:
        """The abstract getting a question by ID from the data storage.

        Args:
            question_id (int): The ID of the question.

        Returns:
            Any | None: The question data if exists.
        """

    @abstractmethod
    async def get_questions_by_quiz(self, quiz_id: int) -> Iterable[Any] | None:
        """The abstract getting questions by quiz from the data storage.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Iterable[Any] | None: The collection of questions for the given quiz.
        """

    @abstractmethod
    async def add_question(self, data: QuestionIn) -> Any | None:
        """The abstract adding a new question to the data storage.

        Args:
            data (QuestionIn): The attributes of the question.

        Returns:
            Any | None: The newly created question.
        """

    @abstractmethod
    async def update_question(
        self,
        question_id: int,
        data: QuestionIn,
    ) -> Any | None:
        """The abstract updating question data in the data storage.

        Args:
            question_id (int): The ID of the question.
            data (QuestionIn): The updated attributes of the question.

        Returns:
            Any | None: The updated question.
        """

    @abstractmethod
    async def delete_question(self, question_id: int) -> bool:
        """The abstract removing a question from the data storage.

        Args:
            question_id (int): The ID of the question.

        Returns:
            bool: Success of the operation.
        """