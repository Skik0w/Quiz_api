"""Module containing history repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable
from pydantic import UUID4
from quizapi.core.domain.history import HistoryIn

class IHistoryRepository(ABC):
    """An abstract class representing protocol of history repository."""

    @abstractmethod
    async def get_all_histories(self) -> Iterable[Any]:
        """The abstract getting all histories from the data storage.

        Returns:
            Iterable[Any]: The collection of all histories.
        """

    @abstractmethod
    async def get_history_by_id(self, history_id: int) -> Any | None:
        """The abstract getting a history by ID from the data storage.

        Args:
            history_id (int): The ID of the history.

        Returns:
            Any | None: The history data if exists.
        """

    @abstractmethod
    async def get_history_by_player(self, player_id: UUID4) -> Iterable[Any] | None:
        """The abstract getting histories by player from the data storage.

        Args:
            player_id (UUID4): The ID of the player.

        Returns:
            Iterable[Any] | None: The collection of all histories by player.
        """

    @abstractmethod
    async def add_history(self, data: HistoryIn, total_questions: int, effectiveness: float) -> Any | None:
        """The abstract adding a new history to the data storage.

        Args:
            data (HistoryIn): The attributes of the history.
            total_questions (int): The total number of questions in the quiz.
            effectiveness (float): The calculated effectiveness percentage.

        Returns:
            Any | None: The newly created history.
        """

    @abstractmethod
    async def update_history(
            self,
            history_id: int,
            data: HistoryIn,
            total_questions: int,
            effectiveness: float,
    ) -> Any | None:
        """The abstract updating history data in the data storage.

        Args:
            history_id (int): The ID of the history.
            data (HistoryIn): The attributes of the history.
            total_questions (int): The total number of questions in the quiz.
            effectiveness (float): The calculated effectiveness percentage.

        Returns:
            Any | None: The updated history.
        """

    @abstractmethod
    async def delete_history(self, history_id: int) -> bool:
        """The abstract removing a history from the data storage.

        Args:
            history_id (int): The ID of the history.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_total_questions_by_quiz(self, quiz_id: int) -> Iterable[Any] | None:
        """The abstract getting total questions by quiz from the data storage.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Iterable[Any] | None: The collection of total questions related to the quiz.
        """