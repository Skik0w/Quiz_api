from abc import ABC, abstractmethod
from typing import Iterable, List
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO
from pydantic import UUID4

class ITournamentService(ABC):

    @abstractmethod
    async def get_all_tournaments(self) -> Iterable[TournamentDTO]:
        """ """

    @abstractmethod
    async def get_tournament_by_id(self, tournament_id: int) -> TournamentDTO | None:
        """ """

    @abstractmethod
    async def add_tournament(self, data: TournamentIn) -> Tournament | None:
        """ """

    @abstractmethod
    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
    ) -> Tournament | None:
        """ """

    @abstractmethod
    async def delete_tournament(self, tournament_id: int) -> bool:
        """ """

    @abstractmethod
    async def join_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament | None:
        """ """

    @abstractmethod
    async def leave_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament | None:
        """ """

