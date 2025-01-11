"""Module containing quiz service implementation."""

from typing import Iterable
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.core.repositories.iquiz import IQuizRepository
from quizapi.infrastructure.dto.quizdto import QuizDTO
from quizapi.infrastructure.services.iquiz import IQuizService

class QuizService(IQuizService):
    """A class implementing the quiz service."""

    _repository: IQuizRepository

    def __init__(self, repository: IQuizRepository):
        """The initializer of the `quiz service`.

        Args:
            repository (IQuizRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_all_quizzes(self) -> Iterable[QuizDTO]:
        """The abstract getting all quizzes from the repository.

        Returns:
            Iterable[QuizDTO]: A collection of all quizzes.
        """
        return await self._repository.get_all_quizzes()

    async def get_quiz_by_id(self, quiz_id: int) -> QuizDTO | None:
        """The abstract getting a quiz by ID.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            QuizDTO | None: The quiz data if found, otherwise None.
        """
        return await self._repository.get_quiz_by_id(quiz_id)

    async def add_quiz(self, data: QuizIn) -> Quiz | None:
        """The abstract adding a new quiz entry to the repository.

        Args:
            data (QuizIn): The quiz data.

        Returns:
            Quiz | None: The newly created quiz entry if successful, otherwise None.
        """
        return await self._repository.add_quiz(data)

    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn
    ) -> Quiz | None:
        """The abstract updating an existing quiz entry in the repository.

        Args:
            quiz_id (int): The ID of the quiz entry.
            data (QuizIn): The updated quiz data.

        Returns:
            Quiz | None: The updated quiz entry if successful, otherwise None.
        """
        return await self._repository.update_quiz(
            quiz_id=quiz_id,
            data=data,
        )

    async def delete_quiz(self, quiz_id: int) -> bool:
        """The abstract removing a quiz entry from the repository.

        Args:
            quiz_id (int): The ID of the quiz entry.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_quiz(quiz_id)

    async def share_quiz(self, quiz_id: int) -> Quiz | None:
        """The abstract sharing a quiz by updating its status.

        Args:
            quiz_id (int): The ID of the quiz entry.

        Returns:
            Quiz | None: The updated quiz entry if successful, otherwise None.
        """
        quiz = await self.get_quiz_by_id(quiz_id)
        return await self._repository.update_quiz(
            quiz_id=quiz_id,
            data=QuizIn(
                title=quiz.title,
                description=quiz.description,
                shared=True,
                reward=quiz.reward,
            )
        )