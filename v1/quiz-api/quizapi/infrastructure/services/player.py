from typing import Iterable
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.core.repositories.iplayer import IPlayerRepository
from quizapi.infrastructure.services.iplayer import IPlayerService
from quizapi.core.domain.store import Reward, RewardIn

class PlayerService(IPlayerService):

    _repository: IPlayerRepository

    def __init__(self, repository: IPlayerRepository):

        self._repository = repository

    async def get_player_by_id(self, player_id: int) -> Player | None:
        return await self._repository.get_player_by_id(player_id)

    async def get_player_by_name(self, name: str) -> Player | None:
        return await self._repository.get_player_by_name(name)

    async def get_all_players(self) -> Iterable[Player]:
        return await self._repository.get_all_players()

    async def add_player(self, player: PlayerIn) -> None:
        await self._repository.add_player(player)

    async def update_player(self, player_id: int, data: PlayerIn) -> Player | None:
        return await self._repository.update_player(player_id, data)

    async def delete_player(self, player_id: int) -> bool:
        return await self._repository.delete_player(player_id)

    async def get_player_rewards(self, player_id: int) -> Iterable[Reward]:
        return await self._repository.get_player_rewards(player_id)
