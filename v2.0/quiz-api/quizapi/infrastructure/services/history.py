"""Module containing history service implementation."""

from typing import Iterable
from quizapi.core.domain.history import History, HistoryIn
from quizapi.core.repositories.ihistory import IHistoryRepository
from quizapi.infrastructure.dto.historydto import HistoryDTO
from quizapi.infrastructure.dto.questiondto import QuestionDTO
from quizapi.infrastructure.services.ihistory import IHistoryService

from pydantic import UUID4

class HistoryService(IHistoryService):
    """A class implementing the history service."""

    _repository: IHistoryRepository

    def __init__(self, repository: IHistoryRepository):
        """The initializer of the `history service`.

        Args:
            repository (IHistoryRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_all_histories(self) -> Iterable[HistoryDTO]:
        """The abstract getting all histories from the repository.

        Returns:
            Iterable[HistoryDTO]: A collection of all histories.
        """
        return await self._repository.get_all_histories()

    async def get_history_by_id(self, history_id: int) -> HistoryDTO | None:
        """The abstract getting a history by ID.

        Args:
            history_id (int): The ID of the history.

        Returns:
            HistoryDTO | None: The history data if found, otherwise None.
        """
        return await self._repository.get_history_by_id(history_id)

    async def get_history_by_player(self, player_id: UUID4) -> Iterable[HistoryDTO] | None:
        """The abstract getting histories by player ID.

        Args:
            player_id (UUID4): The UUID of the player.

        Returns:
            Iterable[HistoryDTO] | None: A collection of histories belonging to the player.
        """
        return await self._repository.get_history_by_player(player_id)

    async def add_history(self, data: HistoryIn) -> History | None:
        """The abstract adding a new history entry to the repository.

        Args:
            data (HistoryIn): The history data.

        Returns:
            History | None: The newly created history entry if successful, otherwise None.
        """
        total_questions = await self._repository.get_total_questions_by_quiz(data.quiz_id)
        total_questions = len(list(total_questions))
        if total_questions > 0:
            effectiveness = data.correct_answers / total_questions
            return await self._repository.add_history(
                data=data,
                total_questions=total_questions,
                effectiveness=effectiveness,
            )
        return None

    async def update_history(
            self,
            history_id: int,
            data: HistoryIn
    ) -> History | None:
        """The abstract updating an existing history entry in the repository.

        Args:
            history_id (int): The ID of the history entry.
            data (HistoryIn): The updated history data.

        Returns:
            History | None: The updated history entry if successful, otherwise None.
        """
        existing_history = await self._repository.get_history_by_id(history_id)
        if not existing_history:
            return None

        total_questions = await self._repository.get_total_questions_by_quiz(data.quiz_id)

        if not total_questions:
            return None

        total_questions_count = len(list(total_questions))
        effectiveness = data.correct_answers / total_questions_count if total_questions_count > 0 else 0.0

        updated = await self._repository.update_history(
            history_id=history_id,
            data=data,
            total_questions=total_questions_count,
            effectiveness=effectiveness,
        )
        return updated

    async def delete_history(self, history_id: int) -> bool:
        """The abstract removing a history entry from the repository.

        Args:
            history_id (int): The ID of the history entry.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_history(history_id)

    async def get_total_questions_by_quiz(self, quiz_id: int) -> Iterable[QuestionDTO] | None:
        """The abstract getting the total number of questions for a given quiz.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Iterable[QuestionDTO] | None: A collection of questions associated with the quiz.
        """
        return await self._repository.get_total_questions_by_quiz(quiz_id)