from typing import Iterable
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.core.repositories.iplayer import IPlayerRepository
from quizapi.infrastructure.repositories.db import players

class PlayerMockRepository(IPlayerRepository):

    async def get_player_by_id(self, player_id: int) -> Player | None:
        return next(
            (obj for obj in players if obj.id == player_id), None
        )

    async def get_all_players(self) -> Iterable[Player]:
        return players

    async def add_player(self, player: PlayerIn) -> None:
        players.append(player)

    async def update_player(
            self,
            player_id: int,
            data: PlayerIn
    ) -> Player | None:
        player_pos = next(
            (index for index, player in enumerate(players) if player.id == player_id),None
        )
        if player_pos is None:
            return None
        updated_player = Player(id=player_id, **data.model_dump())
        players[player_pos] = updated_player
        return players[player_pos]

    async def delete_player(self, player_id: int) -> bool:
        if player_pos := \
                next(filter(lambda x: x.id == player_id, players)):
            players.remove(player_pos)
            return True