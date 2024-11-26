from typing import Iterable
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.core.repositories.iplayer import IPlayerRepository
from quizapi.infrastructure.repositories.db import players
from quizapi.core.domain.store import Reward, RewardIn

class PlayerMockRepository(IPlayerRepository):

    async def get_player_by_id(self, player_id: int) -> Player | None:
        return next(
            (obj for obj in players if obj.id == player_id), None
        )

    async def get_player_by_name(self, name: str) -> Player | None:
        return next(
            (obj for obj in players if obj.username == name), None
        )

    async def get_all_players(self) -> Iterable[Player]:
        return players

    async def add_player(self, player: PlayerIn) -> None:
        players.append(player)

    async def update_player(self, player_id: int, data: PlayerIn) -> Player | None:
        if player_pos := \
                next(filter(lambda p: p.id == player_id, players)):
            players[player_pos] = data
            return Player(id=0, **data.model_dump())
        return None

    async def delete_player(self, player_id: int) -> bool:
        if player_pos := \
                next(filter(lambda p: p.id == player_id, players)):
            players.remove(player_pos)
            return True

    async def get_player_rewards(self, player_id: int) -> Iterable[Reward]:
        if player := next((obj for obj in players if obj.id == player_id), None):
            return player.rewards
        return []