"""Module containing player service abstractions."""

from abc import ABC, abstractmethod
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.infrastructure.dto.playerdto import PlayerDTO
from quizapi.infrastructure.dto.tokendto import TokenDTO
from pydantic import UUID5

class IPlayerService(ABC):
    """An abstract class representing protocol of player service."""

    @abstractmethod
    async def register_player(self, player: PlayerIn) -> PlayerDTO | None:
        """The abstract registering a new player in the repository.

        Args:
            player (PlayerIn): The attributes of the player.

        Returns:
            PlayerDTO | None: The newly registered player if successful.
        """

    @abstractmethod
    async def authenticate_player(self, player: PlayerIn) -> TokenDTO | None:
        """The abstract authenticating a player based on credentials.

        Args:
            player (PlayerIn): The credentials of the player.

        Returns:
            TokenDTO | None: The authentication token if successful.
        """

    @abstractmethod
    async def get_player_by_uuid(self, uuid: UUID5) -> PlayerDTO | None:
        """The abstract getting a player by UUID from the repository.

        Args:
            uuid (UUID5): The UUID of the player.

        Returns:
            PlayerDTO | None: The player data if exists.
        """

    async def get_player_by_email(self, email: str) -> PlayerDTO | None:
        """The abstract getting a player by email from the repository.

        Args:
            email (str): The email address of the player.

        Returns:
            PlayerDTO | None: The player data if exists.
        """

    async def get_player_by_username(self, name: str) -> PlayerDTO | None:
        """The abstract getting a player by username from the repository.

        Args:
            name (str): The username of the player.

        Returns:
            PlayerDTO | None: The player data if exists.
        """

    @abstractmethod
    async def show_balance(self, player_id: UUID5) -> int | None:
        """The abstract getting the balance of a player.

        Args:
            player_id (UUID5): The UUID of the player.

        Returns:
            int | None: The balance of the player if exists.
        """