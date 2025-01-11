"""Module containing player database repository implementation."""

from typing import Any
from asyncpg import Record # type: ignore

from pydantic import UUID5

from sqlalchemy import select
from quizapi.core.repositories.iplayer import IPlayerRepository
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.db import player_table, database
from quizapi.infrastructure.utils.password import hash_password

class PlayerRepository(IPlayerRepository):
    """A class implementing the player repository."""

    async def register_player(self, player: PlayerIn) -> Any | None:
        """Adding a new player to the database.

        Args:
            player (PlayerIn): The player data.

        Returns:
            Any | None: The newly created player record if successful, otherwise None.
        """
        if await self.get_player_by_email(player.email):
            return None

        if await self.get_player_by_username(player.username):
            return None

        player.password = hash_password(player.password)

        query = player_table.insert().values(
            **player.model_dump(),
            balance = 0,
        )
        new_player_uuid = await database.execute(query)

        return  await self.get_player_by_uuid(new_player_uuid)

    async def get_player_by_uuid(self, uuid: UUID5) -> Any | None:
        """Getting a player by UUID.

        Args:
            uuid (UUID5): The UUID of the player.

        Returns:
            Any | None: The player record if found, otherwise None.
        """
        query = (player_table
                 .select()
                 .where(player_table.c.id == uuid)
                 )
        player = await database.fetch_one(query)
        return player

    async def get_player_by_email(self, email: str) -> Any | None:
        """Getting a player by email.

        Args:
            email (str): The email of the player.

        Returns:
            Any | None: The player record if found, otherwise None.
        """
        query = (player_table
                 .select()
                 .where(player_table.c.email == email)
                 )
        player = await database.fetch_one(query)
        return player

    async def get_player_by_username(self, username: str) -> Any | None:
        """Getting a player by username.

        Args:
            username (str): The username of the player.

        Returns:
            Any | None: The player record if found, otherwise None.
        """
        query = (player_table
                 .select()
                 .where(player_table.c.username == username)
                 )
        player = await database.fetch_one(query)
        return player

    async def show_balance(self, player_id: UUID5) -> Any | None:
        """Getting a player's balance.

        Args:
            player_id (UUID5): The UUID of the player.

        Returns:
            Any | None: The player's balance if found, otherwise None.
        """
        query = (
            select(
                player_table.c.balance,
            ).where(
                player_table.c.id == player_id
            )
        )
        balance = await database.fetch_one(query)
        if not balance:
            return None
        return balance["balance"]