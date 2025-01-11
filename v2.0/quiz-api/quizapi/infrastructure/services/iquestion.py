"""Module containing question service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.infrastructure.dto.questiondto import QuestionDTO


class IQuestionService(ABC):
    """An abstract class representing protocol of question service."""

    @abstractmethod
    async def get_all_questions(self) -> Iterable[QuestionDTO]:
        """The abstract getting all questions from the repository.

        Returns:
            Iterable[QuestionDTO]: The collection of all questions.
        """

    @abstractmethod
    async def get_question_by_id(self, question_id: int) -> QuestionDTO | None:
        """The abstract getting a question by ID from the repository.

        Args:
            question_id (int): The ID of the question.

        Returns:
            QuestionDTO | None: The question data if exists.
        """

    @abstractmethod
    async def get_questions_by_quiz(self, quiz_id: int) -> Iterable[QuestionDTO] | None:
        """The abstract getting all questions associated with a quiz from the repository.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Iterable[QuestionDTO] | None: The collection of questions if exists.
        """

    @abstractmethod
    async def add_question(self, data: QuestionIn) -> Question | None:
        """The abstract adding a new question to the repository.

        Args:
            data (QuestionIn): The attributes of the question.

        Returns:
            Question | None: The newly created question if successful.
        """

    @abstractmethod
    async def update_question(
        self,
        question_id: int,
        data: QuestionIn,
    ) -> Question | None:
        """The abstract updating a question in the repository.

        Args:
            question_id (int): The ID of the question.
            data (QuestionIn): The updated attributes of the question.

        Returns:
            Question | None: The updated question if successful.
        """

    @abstractmethod
    async def delete_question(self, question_id: int) -> bool:
        """The abstract removing a question from the repository.

        Args:
            question_id (int): The ID of the question.

        Returns:
            bool: Success of the operation.
        """