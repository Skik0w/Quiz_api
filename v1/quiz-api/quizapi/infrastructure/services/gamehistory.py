from typing import Iterable
from quizapi.core.domain.gamehistory import GameHistory, GameHistoryIn
from quizapi.core.repositories.igamehistory import IGameHistoryRepository
from quizapi.infrastructure.services.igamehistory import IGameHistoryService

class GameHistoryService(IGameHistoryService):

    _repository: IGameHistoryRepository

    def __init__(self, repository: IGameHistoryRepository):

        self._repository = repository

    async def add_game_history(self, data: GameHistoryIn) -> None:
        await self._repository.add_game_history(data)

    async def get_game_history(self, player_id: int) -> Iterable[GameHistory]:
        return await self._repository.get_game_history(player_id)
