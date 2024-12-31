from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from quizapi.db import tournament_table, database
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.core.repositories.itournament import ITournamentRepository


class TournamentRepository(ITournamentRepository):

    async def get_all_tournaments(self) -> Iterable[Any]:
        query = (
            select(
                tournament_table.c.id.label("tournament_id"),
                tournament_table.c.name.label("tournament_name"),
                tournament_table.c.description.label("tournament_description"),
                tournament_table.c.quizzes.label("tournament_quizzes"),
                tournament_table.c.players.label("tournament_players"),
                tournament_table.c.results.label("tournament_results"),
            )
            .order_by(tournament_table.c.id.asc())
        )

        tournaments = await database.fetch_all(query)
        return [TournamentDTO.from_record(tournament) for tournament in tournaments]

    async def get_tournament_by_id(self, tournament_id: int) -> Any | None:
        query = (
            select(
                tournament_table.c.id.label("tournament_id"),
                tournament_table.c.name.label("tournament_name"),
                tournament_table.c.description.label("tournament_description"),
                tournament_table.c.quizzes.label("tournament_quizzes"),
                tournament_table.c.players.label("tournament_players"),
                tournament_table.c.results.label("tournament_results"),
            )
            .where(tournament_table.c.id == tournament_id)
            .order_by(tournament_table.c.id.asc())
        )

        tournament = await database.fetch_one(query)
        return TournamentDTO.from_record(tournament) if tournament else None

    async def create_tournament(self, data: TournamentIn) -> Any | None:
        query = tournament_table.insert().values(**data.dict())
        new_tournament_id = await database.execute(query)
        return await self._get_by_id(new_tournament_id)

    async def add_player(self, tournament_id: int, player_id: str) -> Any | None:
        query = (
            tournament_table.update()
            .where(tournament_table.c.id == tournament_id)
            .values(players=tournament_table.c.players.op("||")([player_id]))
        )
        await database.execute(query)
        return await self._get_by_id(tournament_id)

    async def remove_player(self, tournament_id: int, player_id: str) -> Any | None:
        query = (
            tournament_table.update()
            .where(tournament_table.c.id == tournament_id)
            .values(players=tournament_table.c.players.op("-")([player_id]))
        )
        await database.execute(query)
        return await self._get_by_id(tournament_id)

    async def add_results(self, tournament_id: int, results: dict[str, int]) -> Any | None:
        query = (
            tournament_table.update()
            .where(tournament_table.c.id == tournament_id)
            .values(results=tournament_table.c.results.op("||")(results))
        )
        await database.execute(query)
        return await self._get_by_id(tournament_id)

    async def update_quizzes(self, tournament_id: int, quiz_ids: list[int]) -> Any | None:
        query = (
            tournament_table.update()
            .where(tournament_table.c.id == tournament_id)
            .values(quizzes=tournament_table.c.quizzes.op("||")(quiz_ids))
        )
        await database.execute(query)
        return await self._get_by_id(tournament_id)

    async def delete_tournament(self, tournament_id: int) -> bool:
        query = tournament_table.delete().where(tournament_table.c.id == tournament_id)
        await database.execute(query)
        return True

    async def _get_by_id(self, tournament_id: int) -> Record | None:
        query = (
            tournament_table.select()
            .where(tournament_table.c.id == tournament_id)
            .order_by(tournament_table.c.id.asc())
        )
        return await database.fetch_one(query)
