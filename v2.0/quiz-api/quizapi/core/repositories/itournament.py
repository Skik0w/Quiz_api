"""Module containing tournament repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable
from quizapi.core.domain.tournament import TournamentIn
from pydantic import UUID4

class ITournamentRepository(ABC):
    """An abstract class representing protocol of tournament repository."""

    @abstractmethod
    async def get_all_tournaments(self) -> Iterable[Any]:
        """The abstract getting all tournaments from the data storage.

        Returns:
            Iterable[Any]: The collection of all tournaments.
        """

    @abstractmethod
    async def get_tournament_by_id(self, tournament_id: int) -> Any | None:
        """The abstract getting a tournament by ID from the data storage.

        Args:
            tournament_id (int): The ID of the tournament.

        Returns:
            Any | None: The tournament data if exists.
        """

    @abstractmethod
    async def add_tournament(self, data: TournamentIn) -> Any | None:
        """The abstract adding a new tournament to the data storage.

        Args:
            data (TournamentIn): The attributes of the tournament.

        Returns:
            Any | None: The newly created tournament.
        """

    @abstractmethod
    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
    ) -> Any | None:
        """The abstract updating tournament data in the data storage.

        Args:
            tournament_id (int): The ID of the tournament.
            data (TournamentIn): The updated attributes of the tournament.

        Returns:
            Any | None: The updated tournament.
        """

    @abstractmethod
    async def delete_tournament(self, tournament_id: int) -> bool:
        """The abstract removing a tournament from the data storage.

        Args:
            tournament_id (int): The ID of the tournament.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def join_tournament(self, tournament_id: int, player_uuid: UUID4) -> Any | None:
        """The abstract joining a tournament in the data storage.

        Args:
            tournament_id (int): The ID of the tournament.
            player_uuid (UUID4): The UUID of the player joining.

        Returns:
            Any | None: The updated tournament data if successful.
        """

    @abstractmethod
    async def leave_tournament(self, tournament_id: int, player_uuid: UUID4) -> Any | None:
        """The abstract leaving a tournament in the data storage.

        Args:
            tournament_id (int): The ID of the tournament.
            player_uuid (UUID4): The UUID of the player leaving.

        Returns:
            Any | None: The updated tournament data if successful.
        """
