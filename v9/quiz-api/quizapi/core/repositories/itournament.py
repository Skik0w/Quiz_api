from abc import ABC, abstractmethod
from typing import Any, Iterable, Dict, List
from quizapi.core.domain.tournament import TournamentIn
from pydantic import UUID4

class ITournamentRepository(ABC):

    @abstractmethod
    async def get_all_tournaments(self) -> Iterable[Any]:
        """ """

    @abstractmethod
    async def get_tournament_by_id(self, tournament_id: int) -> Any | None:
        """ """

    @abstractmethod
    async def create_tournament(self, data: TournamentIn) -> Any | None:
        """ """

    @abstractmethod
    async def join_tournament(self, tournament_id: int, player_id: UUID4) -> Any | None:
        """ """

    @abstractmethod
    async def leave_tournament(self, tournament_id: int, player_id: UUID4) -> Any | None:
        """ """

    @abstractmethod
    async def add_results(self, tournament_id: int, results: Dict[UUID4, int]) -> Any | None:
        """ """

    @abstractmethod
    async def update_quizzes(
            self,
            tournament_id: int,
            quiz_ids: List[int]
    ) -> Any | None:
        """ """