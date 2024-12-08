from typing import Any, Iterable
from asyncpg import Record # type: ignore
from sqlalchemy import select, join
from quizapi.core.repositories.iplayer import IPlayerRepository
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.db import player_table, database
from quizapi.infrastructure.dto.playerdto import PlayerDTO

class PlayerRepository(IPlayerRepository):

    async def get_all_players(self) -> Iterable[Any]:
        query = player_table.select().order_by(player_table.c.id.asc())
        players = await database.fetch_all(query)
        return [Player(**dict(player)) for player in players]

    async def get_player_by_id(self, player_id: int) -> Record | None:
        player = await self._get_by_id(player_id)
        return Player(**dict(player)) if player else None

    async def add_player(self, data: PlayerIn) -> Any | None:
        query = player_table.insert().values(**data.model_dump())
        new_player_id = await database.execute(query)
        new_player = await self._get_by_id(new_player_id)
        return Player(**dict(new_player)) if new_player else None

    async def update_player(
            self,
            player_id: int,
            data: PlayerIn,
    ) -> Any | None:
        if self._get_by_id(player_id):
            query = player_table.update().where(player_table.c.id == player_id).values(**data.model_dump())
            await database.execute(query)
            player = await self._get_by_id(player_id)
            return Player(**dict(player)) if player else None
        return None

    async def delete_player(self, player_id: int) -> bool:
        if self._get_by_id(player_id):
            query = player_table.delete().where(player_table.c.id == player_id)
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, player_id: int) -> Record | None:
        query = player_table.select().where(player_table.c.id == player_id).order_by(player_table.c.username.asc())
        return await database.fetch_one(query)