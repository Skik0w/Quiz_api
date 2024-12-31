from abc import ABC, abstractmethod
from typing import Iterable, Dict, List
from pydantic import UUID4
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO


class ITournamentService(ABC):

    @abstractmethod
    async def get_all_tournaments(self) -> Iterable[TournamentDTO]:
        """ """

    @abstractmethod
    async def get_tournament_by_id(self, tournament_id: int) -> TournamentDTO | None:
        """ """

    @abstractmethod
    async def create_tournament(self, data: TournamentIn) -> Tournament | None:
        """ """

    @abstractmethod
    async def join_tournament(self, tournament_id: int, player_id: UUID4) -> Tournament | None:
        """ """

    @abstractmethod
    async def leave_tournament(self, tournament_id: int, player_id: UUID4) -> Tournament | None:
        """ """

    @abstractmethod
    async def add_results(self, tournament_id: int, results: Dict[UUID4, int]) -> Tournament | None:
        """ """

    @abstractmethod
    async def update_quizzes(
            self,
            tournament_id: int,
            quiz_ids: List[int]
    ) -> Tournament | None:
        """ """
