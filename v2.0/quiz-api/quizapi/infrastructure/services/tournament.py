"""Module containing tournament service implementation."""

from typing import Iterable
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.core.repositories.itournament import ITournamentRepository
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO
from quizapi.infrastructure.services.itournament import ITournamentService
from pydantic import UUID4

class TournamentService(ITournamentService):
    """A class implementing the tournament service."""

    _repository: ITournamentRepository

    def __init__(self, repository: ITournamentRepository):
        """The initializer of the `tournament service`.

        Args:
            repository (ITournamentRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_all_tournaments(self) -> Iterable[TournamentDTO]:
        """The abstract getting all tournaments from the repository.

        Returns:
            Iterable[TournamentDTO]: A collection of all tournaments.
        """
        return await self._repository.get_all_tournaments()

    async def get_tournament_by_id(self, tournament_id: int) -> TournamentDTO | None:
        """The abstract getting a tournament by ID from the repository.

        Args:
            tournament_id (int): The ID of the tournament.

        Returns:
            TournamentDTO | None: The tournament data if found, otherwise None.
        """
        return await self._repository.get_tournament_by_id(tournament_id)

    async def add_tournament(self, data: TournamentIn) -> Tournament | None:
        """The abstract adding a new tournament to the repository.

        Args:
            data (TournamentIn): The tournament data.

        Returns:
            Tournament | None: The newly created tournament if successful, otherwise None.
        """
        return await self._repository.add_tournament(data)

    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
    ) -> Tournament | None:
        """The abstract updating a tournament in the repository.

        Args:
            tournament_id (int): The ID of the tournament.
            data (TournamentIn): The updated tournament data.

        Returns:
            Tournament | None: The updated tournament if successful, otherwise None.
        """
        return await self._repository.update_tournament(
            tournament_id=tournament_id,
            data=data,
        )

    async def delete_tournament(self, tournament_id: int) -> bool:
        """The abstract removing a tournament from the repository.

        Args:
            tournament_id (int): The ID of the tournament.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_tournament(tournament_id)

    async def join_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament:
        """The abstract adding a player to a tournament in the repository.

        Args:
            tournament_id (int): The ID of the tournament.
            player_uuid (UUID4): The UUID of the player.

        Returns:
            Tournament: The updated tournament with the player added.
        """
        return await self._repository.join_tournament(tournament_id, player_uuid)

    async def leave_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament:
        """The abstract removing a player from a tournament in the repository.

        Args:
            tournament_id (int): The ID of the tournament.
            player_uuid (UUID4): The UUID of the player.

        Returns:
            Tournament: The updated tournament with the player removed.
        """
        return await self._repository.leave_tournament(tournament_id, player_uuid)