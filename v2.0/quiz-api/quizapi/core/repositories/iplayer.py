"""Module containing player repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any
from quizapi.core.domain.player import PlayerIn
from pydantic import UUID5

class IPlayerRepository(ABC):
    """An abstract class representing protocol of player repository."""

    @abstractmethod
    async def get_player_by_uuid(self, uuid: UUID5) -> Any | None:
        """The abstract getting a player by UUID from the data storage.

        Args:
            uuid (UUID5): The UUID of the player.

        Returns:
            Any | None: The player data if exists.
        """

    @abstractmethod
    async def get_player_by_email(self, email: str) -> Any | None:
        """The abstract getting a player by email from the data storage.

        Args:
            email (str): The email of the player.

        Returns:
            Any | None: The player data if exists.
        """

    @abstractmethod
    async def get_player_by_username(self, username: str) -> Any | None:
        """The abstract getting a player by username from the data storage.

        Args:
            username (str): The username of the player.

        Returns:
            Any | None: The player data if exists.
        """

    @abstractmethod
    async def register_player(self, player: PlayerIn) -> Any | None:
        """The abstract registering a new player in the data storage.

        Args:
            player (PlayerIn): The attributes of the player.

        Returns:
            Any | None: The newly created player.
        """

    @abstractmethod
    async def show_balance(self, player_id: UUID5) -> Any | None:
        """The abstract getting a player's balance from the data storage.

        Args:
            player_id (UUID5): The UUID of the player.

        Returns:
            Any | None: The player's balance if exists.
        """