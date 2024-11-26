"""Module containing player repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.core.domain.store import Reward, RewardIn

class IPlayerRepository(ABC):

    @abstractmethod
    async def get_player_by_id(self, player_id: int) -> Player | None:
        """The abstract getting a player by id from the data storage.

        Args:
            player_id (int): The id of the player.

        Returns:
            Player | None: The player data if exists.
        """

    @abstractmethod
    async def get_player_by_name(self, name: str) -> Player | None:
        """The abstract getting a player by name from the data storage.

        Args:
            name (int): The name of the player.

        Returns:
            Player | None: The player data if exists.
        """

    @abstractmethod
    async def get_all_players(self) -> Iterable[Player]:
        """The abstract getting all players from the data storage.

        Returns:
            Iterable[Player]: The collection of all players.
        """

    @abstractmethod
    async def add_player(self, player: PlayerIn) -> None:
        """The abstract adding a new player to the data storage.

        Args:
            player (PlayerIn): The attributes of the player.
        """

    @abstractmethod
    async def update_player(self, player_id: int, player: PlayerIn) -> Player | None:
        """The abstract updating player data in the data storage.

        Args:
            player_id (int): The player ID.
            player (Player): The attributes of the player.

        Returns:
            Player | None: The updated player data if successful.
        """

    @abstractmethod
    async def delete_player(self, player_id: int) -> bool:
        """The abstract removing a player from the data storage.

        Args:
            player_id (int): The player ID.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_player_rewards(self, player_id: int) -> Iterable[Reward]:
        """The abstract getting all rewards of a player from the data storage.

        Args:
            player_id (int): The ID of the player.

        Returns:
            Iterable[Reward]: The collection of rewards for the player.
        """