"""Module containing player service implementation."""

from quizapi.core.domain.player import Player, PlayerIn
from quizapi.core.repositories.iplayer import IPlayerRepository
from quizapi.infrastructure.dto.playerdto import PlayerDTO
from quizapi.infrastructure.dto.tokendto import TokenDTO
from quizapi.infrastructure.services.iplayer import IPlayerService
from pydantic import UUID4
from quizapi.infrastructure.utils.password import verify_password
from quizapi.infrastructure.utils.token import generate_player_token

class PlayerService(IPlayerService):
    """A class implementing the player service."""

    _repository: IPlayerRepository

    def __init__(self, repository: IPlayerRepository):
        """The initializer of the `player service`.

        Args:
            repository (IPlayerRepository): The reference to the repository.
        """
        self._repository = repository

    async def register_player(self, player: PlayerIn) -> PlayerDTO | None:
        """The abstract adding a new player to the repository.

        Args:
            player (PlayerIn): The attributes of the player.

        Returns:
            PlayerDTO | None: The newly created player if successful, otherwise None.
        """
        return await self._repository.register_player(player)

    async def authenticate_player(self, player: PlayerIn) -> TokenDTO | None:
        """The abstract authenticating a player based on credentials.

        Args:
            player (PlayerIn): The credentials of the player.

        Returns:
            TokenDTO | None: The authentication token if successful, otherwise None.
        """
        if player_data := await self._repository.get_player_by_email(player.email):
            if verify_password(player.password, player_data.password):
                token_details = generate_player_token(player_data.id)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)
            return None
        return None

    async def get_player_by_uuid(self, uuid: UUID4) -> PlayerDTO | None:
        """The abstract getting a player by UUID from the repository.

        Args:
            uuid (UUID4): The UUID of the player.

        Returns:
            PlayerDTO | None: The player data if found, otherwise None.
        """
        return await self._repository.get_player_by_uuid(uuid)

    async def get_player_by_email(self, email: str) -> PlayerDTO | None:
        """The abstract getting a player by email from the repository.

        Args:
            email (str): The email address of the player.

        Returns:
            PlayerDTO | None: The player data if found, otherwise None.
        """
        return await self._repository.get_player_by_email(email)

    async def get_player_by_username(self, username: str) -> PlayerDTO | None:
        """The abstract getting a player by username from the repository.

        Args:
            username (str): The username of the player.

        Returns:
            PlayerDTO | None: The player data if found, otherwise None.
        """
        return await self._repository.get_player_by_username(username)

    async def show_balance(self, player: UUID4) -> int | None:
        """The abstract getting the balance of a player from the repository.

        Args:
            player (UUID4): The UUID of the player.

        Returns:
            int | None: The player's balance if found, otherwise None.
        """
        return await self._repository.show_balance(player)