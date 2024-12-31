from typing import Iterable, List
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.core.repositories.itournament import ITournamentRepository
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO
from quizapi.infrastructure.services.itournament import ITournamentService
from pydantic import UUID4

class TournamentService(ITournamentService):

    _repository: ITournamentRepository

    def __init__(self, repository: ITournamentRepository):
        self._repository = repository

    async def get_all_tournaments(self) -> Iterable[TournamentDTO]:
        return await self._repository.get_all_tournaments()

    async def get_tournament_by_id(self, tournament_id: int) -> TournamentDTO | None:
        return await self._repository.get_tournament_by_id(tournament_id)

    async def add_tournament(self, data: TournamentIn) -> Tournament | None:
        return await self._repository.add_tournament(data)

    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
            #participants: List[UUID4]
    ) -> Tournament | None:
        return await self._repository.update_tournament(
            tournament_id=tournament_id,
            data=data,
            #participants=participants
        )

    async def delete_tournament(self, tournament_id: int) -> bool:
        return await self._repository.delete_tournament(tournament_id)

    async def join_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament:
        return await self._repository.join_tournament(tournament_id, player_uuid)

    async def leave_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament:
        return await self._repository.leave_tournament(tournament_id, player_uuid)