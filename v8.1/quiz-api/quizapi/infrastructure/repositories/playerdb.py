from typing import Any, Iterable
from asyncpg import Record # type: ignore
from pydantic import UUID5

from quizapi.core.repositories.iplayer import IPlayerRepository
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.db import player_table, database
from quizapi.infrastructure.utils.password import hash_password

class PlayerRepository(IPlayerRepository):

    async def register_player(self, player: PlayerIn) -> Any | None:
        if await self.get_player_by_email(player.email):
            return None
        player.password = hash_password(player.password)

        query = player_table.insert().values(**player.model_dump())
        new_player_uuid = await database.execute(query)

        return  await self.get_player_by_uuid(new_player_uuid)

    async def get_player_by_uuid(self, uuid: UUID5) -> Any | None:
        query = (player_table
                 .select()
                 .where(player_table.c.id == uuid)
                 )
        player = await database.fetch_one(query)
        return player

    async def get_player_by_email(self, email: str) -> Any | None:
        query = (player_table
                 .select()
                 .where(player_table.c.email == email)
                 )
        player = await database.fetch_one(query)
        return player