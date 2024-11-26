from typing import Iterable

from quizapi.core.domain.gamehistory import GameHistory, GameHistoryIn
from quizapi.core.repositories.igamehistory import IGameHistoryRepository
from quizapi.infrastructure.repositories.db import game_histories

class GameHistoryMockRepository(IGameHistoryRepository):

    async def add_game_history(self, data: GameHistoryIn) -> None:
        game_histories.append(data)

    async def get_game_history(self, player_id: int) -> Iterable[GameHistory]:
        return [history for history in game_histories if history.user_id == player_id] or []
