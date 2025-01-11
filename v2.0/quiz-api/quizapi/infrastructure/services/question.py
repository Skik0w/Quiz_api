"""Module containing question service implementation."""

from typing import Iterable
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.core.repositories.iquestion import IQuestionRepository
from quizapi.infrastructure.dto.questiondto import QuestionDTO
from quizapi.infrastructure.services.iquestion import IQuestionService

class QuestionService(IQuestionService):
    """A class implementing the question service."""

    _repository: IQuestionRepository

    def __init__(self, repository: IQuestionRepository):
        """The initializer of the `question service`.

        Args:
            repository (IQuestionRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_all_questions(self) -> Iterable[QuestionDTO]:
        """The abstract getting all questions from the repository.

        Returns:
            Iterable[QuestionDTO]: A collection of all questions.
        """
        return await self._repository.get_all_questions()

    async def get_question_by_id(self, question_id: int) -> QuestionDTO | None:
        """The abstract getting a question by ID.

        Args:
            question_id (int): The ID of the question.

        Returns:
            QuestionDTO | None: The question data if found, otherwise None.
        """
        return await self._repository.get_question_by_id(question_id)

    async def get_questions_by_quiz(self, quiz_id: int) -> Iterable[QuestionDTO] | None:
        """The abstract getting questions by quiz ID.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Iterable[QuestionDTO] | None: A collection of questions associated with the quiz.
        """
        return await self._repository.get_questions_by_quiz(quiz_id)

    async def add_question(self, data: QuestionIn) -> None:
        """The abstract adding a new question to the repository.

        Args:
            data (QuestionIn): The question data.

        Returns:
            None
        """
        return await self._repository.add_question(data)

    async def update_question(
        self,
        question_id: int,
        data: QuestionIn,
    ) -> Question | None:
        """The abstract updating a question in the repository.

        Args:
            question_id (int): The ID of the question.
            data (QuestionIn): The updated question data.

        Returns:
            Question | None: The updated question if successful, otherwise None.
        """
        return await self._repository.update_question(
            question_id=question_id,
            data=data,
        )

    async def delete_question(self, question_id: int) -> bool:
        """The abstract removing a question from the repository.

        Args:
            question_id (int): The ID of the question.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_question(question_id)