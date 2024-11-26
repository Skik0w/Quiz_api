from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.gamehistory import GameHistory, GameHistoryIn


class IGameHistoryService(ABC):

    @abstractmethod
    async def add_game_history(self, data: GameHistoryIn) -> None:
        """ """

    @abstractmethod
    async def get_game_history(self, player_id: int) -> Iterable[GameHistory]:
        """ """