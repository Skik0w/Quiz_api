"""Module containing game history repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.gamehistory import GameHistory, GameHistoryIn

class IGameHistoryRepository(ABC):

    @abstractmethod
    async def add_game_history(self, data: GameHistoryIn) -> None:
        """The abstract adding game history data to the data storage.

        Args:
            data (GameHistory): The attributes of the game history.
        """

    @abstractmethod
    async def get_game_history(self, player_id: int) -> Iterable[GameHistory]:
        """The abstract getting all game history for a player from the data storage.

        Args:
            player_id (int): The player id.

        Returns:
            Iterable[GameHistory]: The collection of game history for the player.
        """
