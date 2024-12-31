from typing import Iterable, Dict, List
from uuid import UUID
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.core.repositories.itournament import ITournamentRepository
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO
from quizapi.infrastructure.services.itournament import ITournamentService

class TournamentService(ITournamentService):

    _repository: ITournamentRepository

    def __init__(self, repository: ITournamentRepository):
        self._repository = repository

    async def get_all_tournaments(self) -> Iterable[TournamentDTO]:
        return await self._repository.get_all_tournaments()

    async def get_tournament_by_id(self, tournament_id: int) -> TournamentDTO | None:
        return await self._repository.get_tournament_by_id(tournament_id)

    async def create_tournament(self, data: TournamentIn) -> Tournament | None:
        return await self._repository.create_tournament(data)

    async def join_tournament(self, tournament_id: int, player_id: UUID) -> Tournament | None:
        return await self._repository.add_player(tournament_id, player_id)

    async def leave_tournament(self, tournament_id: int, player_id: UUID) -> Tournament | None:
        return await self._repository.remove_player(tournament_id, player_id)

    async def add_results(self, tournament_id: int, results: Dict[UUID, int]) -> Tournament | None:
        return await self._repository.add_results(tournament_id, results)

    async def update_quizzes(self, tournament_id: int, quiz_ids: List[int]) -> Tournament | None:
        return await self._repository.update_quizzes(tournament_id, quiz_ids)
