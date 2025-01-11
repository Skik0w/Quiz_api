"""Module containing history service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.history import History, HistoryIn
from quizapi.infrastructure.dto.historydto import HistoryDTO
from pydantic import UUID4


class IHistoryService(ABC):
    """An abstract class representing protocol of history service."""

    @abstractmethod
    async def get_all_histories(self) -> Iterable[HistoryDTO]:
        """The abstract getting all histories from the repository.

        Returns:
            Iterable[HistoryDTO]: The collection of all histories.
        """

    @abstractmethod
    async def get_history_by_id(self, history_id: int) -> HistoryDTO | None:
        """The abstract getting a history by ID from the repository.

        Args:
            history_id (int): The ID of the history.

        Returns:
            HistoryDTO | None: The history data if exists.
        """

    @abstractmethod
    async def get_history_by_player(self, player_id: UUID4) -> Iterable[HistoryDTO] | None:
        """The abstract getting histories by player ID from the repository.

        Args:
            player_id (UUID4): The UUID of the player.

        Returns:
            Iterable[HistoryDTO] | None: The collection of histories by player.
        """

    @abstractmethod
    async def add_history(self, data: HistoryIn) -> History | None:
        """The abstract adding a new history entry to the repository.

        Args:
            data (HistoryIn): The attributes of the history.

        Returns:
            History | None: The newly created history entry.
        """
    @abstractmethod
    async def update_history(
            self,
            history_id: int,
            data: HistoryIn
    ) -> History | None:
        """The abstract updating a history entry in the repository.

        Args:
            history_id (int): The ID of the history.
            data (HistoryIn): The updated history attributes.

        Returns:
            History | None: The updated history entry if exists.
        """

    @abstractmethod
    async def delete_history(self, history_id: int) -> bool:
        """The abstract removing a history entry from the repository.

        Args:
            history_id (int): The ID of the history.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_total_questions_by_quiz(self, quiz_id: int) -> int | None:
        """The abstract getting the total number of questions for a quiz.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            int | None: The total number of questions if exists.
        """