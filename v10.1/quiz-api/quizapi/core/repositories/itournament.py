from abc import ABC, abstractmethod
from typing import Any, Iterable, List
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
    async def add_tournament(self, data: TournamentIn) -> Any | None:
        """ """

    @abstractmethod
    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
            #participants: List[UUID4]
    ) -> Any | None:
        """ """

    @abstractmethod
    async def delete_tournament(self, tournament_id: int) -> bool:
        """ """

    @abstractmethod
    async def join_tournament(self, tournament_id: int, player_uuid: UUID4) -> Any | None:
        """ """

    @abstractmethod
    async def leave_tournament(self, tournament_id: int, player_uuid: UUID4) -> Any | None:
        """ """
