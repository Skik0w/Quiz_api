"""Module containing question repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from quizapi.core.domain.question import Question, QuestionIn


class IQuestionRepository(ABC):

    @abstractmethod
    async def get_question_by_id(self, question_id: int) -> Question | None:
        """The abstract getting a question by id from the data storage.

        Args:
            question_id (int): The id of the question.

        Returns:
            Question | None: The question data if exists.
        """

    @abstractmethod
    async def get_all_questions(self) -> Iterable[Question]:
        """The abstract getting all questions from the data storage.

        Returns:
            Iterable[Question]: The collection of all questions.
        """

    @abstractmethod
    async def add_question(self, question: QuestionIn) -> None:
        """The abstract adding a new question to the data storage.

        Args:
            question (Question): The attributes of the question.
        """

    @abstractmethod
    async def update_question(
        self,
        question_id: int,
        question: QuestionIn,
    ) -> Question | None:
        """The abstract updating question data in the data storage.

        Args:
            question_id (int): The question id.
            question (Question): The attributes of the question.

        Returns:
            Question | None: The updated question data if successful.
        """

    @abstractmethod
    async def delete_question(self, question_id: int) -> bool:
        """The abstract removing a question from the data storage.

        Args:
            question_id (int): The question id.

        Returns:
            bool: Success of the operation.
        """