"""Module containing tournament service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO
from pydantic import UUID4

class ITournamentService(ABC):
    """An abstract class representing protocol of tournament service."""

    @abstractmethod
    async def get_all_tournaments(self) -> Iterable[TournamentDTO]:
        """The abstract getting all tournaments.

        Returns:
            Iterable[TournamentDTO]: The collection of all tournaments.
        """

    @abstractmethod
    async def get_tournament_by_id(self, tournament_id: int) -> TournamentDTO | None:
        """The abstract getting a tournament by ID.

        Args:
            tournament_id (int): The ID of the tournament.

        Returns:
            TournamentDTO | None: The tournament data if exists.
        """

    @abstractmethod
    async def add_tournament(self, data: TournamentIn) -> Tournament | None:
        """The abstract adding a new tournament.

        Args:
            data (TournamentIn): The attributes of the tournament.

        Returns:
            Tournament | None: The newly created tournament if successful.
        """

    @abstractmethod
    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
    ) -> Tournament | None:
        """The abstract updating tournament data.

        Args:
            tournament_id (int): The ID of the tournament.
            data (TournamentIn): The updated attributes of the tournament.

        Returns:
            Tournament | None: The updated tournament if successful.
        """

    @abstractmethod
    async def delete_tournament(self, tournament_id: int) -> bool:
        """The abstract removing a tournament.

        Args:
            tournament_id (int): The ID of the tournament.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def join_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament | None:
        """The abstract allowing a player to join a tournament.

        Args:
            tournament_id (int): The ID of the tournament.
            player_uuid (UUID4): The UUID of the player joining the tournament.

        Returns:
            Tournament | None: The tournament with the updated participant list if successful.
        """

    @abstractmethod
    async def leave_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament | None:
        """The abstract allowing a player to leave a tournament.

        Args:
            tournament_id (int): The ID of the tournament.
            player_uuid (UUID4): The UUID of the player leaving the tournament.

        Returns:
            Tournament | None: The tournament with the updated participant list if successful.
        """

