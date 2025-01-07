from typing import Any, Iterable, List
from asyncpg import Record # type: ignore
from pydantic import UUID4
from sqlalchemy import select, join

from quizapi.core.repositories.itournament import ITournamentRepository
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.db import tournament_table, database, quiz_table, player_table
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO

from quizapi.infrastructure.repositories.quizdb import QuizDTO

class TournamentRepository(ITournamentRepository):

    async def get_all_tournaments(self) -> Iterable[Any]:
        query = select(
            tournament_table
        ).order_by(
            tournament_table.c.id.asc()
        )
        tournaments = await database.fetch_all(query)
        return [TournamentDTO.from_record(tournament) for tournament in tournaments]

    async def get_tournament_by_id(self, tournament_id: int) -> Any | None:
        query = select(
            tournament_table
        ).where(
            tournament_table.c.id == tournament_id
        ).order_by(
            tournament_table.c.id.asc()
        )
        tournament = await database.fetch_one(query)
        return TournamentDTO.from_record(tournament) if tournament else None

    async def add_tournament(self, data: TournamentIn) -> None:

        for quiz_id in data.quizzes_id:
            quiz = await self.get_quiz_by_id(quiz_id)
            if not quiz:
                return None


        query = tournament_table.insert().values(
            name= data.name,
            description= data.description,
            participants= [],
            quizzes_id = data.quizzes_id
        )
        new_tournament_id = await database.execute(query)
        new_tournament = await self._get_by_id(new_tournament_id)
        return Tournament(**dict(new_tournament)) if new_tournament else None

    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
            #participants: List[UUID4]
    ) -> Tournament | None:

        for quiz_id in data.quizzes_id:
            quiz = await self.get_quiz_by_id(quiz_id)
            if not quiz:
                return None

        existing_tournament = await self._get_by_id(tournament_id)
        if not existing_tournament:
            return None
        query = (
            tournament_table.update()
            .where(tournament_table.c.id == tournament_id)
            .values(
                name=data.name,
                description=data.description,
                #participants=participants,
                quizzes_id=data.quizzes_id
            )
        )
        await database.execute(query)
        updated_tournament = await self._get_by_id(tournament_id)
        return Tournament(**dict(updated_tournament)) if updated_tournament else None

    async def delete_tournament(self, tournament_id: int) -> bool:
        if self._get_by_id(tournament_id):
            query = tournament_table.delete().where(tournament_table.c.id == tournament_id)
            await database.execute(query)
            return True
        return False

    async def join_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament | None:
        query = (
            select(
                tournament_table.c.participants
            )
            .where(tournament_table.c.id == tournament_id)
        )
        tournament = await database.fetch_one(query)

        if not tournament:
            return None

        participants = tournament["participants"] or []

        if player_uuid in participants:
            return None

        participants.append(player_uuid)
        updated_query = (
            tournament_table.update()
            .where(tournament_table.c.id == tournament_id)
            .values(participants=participants)
            .returning(tournament_table)
        )
        updated_participants = await database.fetch_one(updated_query)
        return Tournament(**dict(updated_participants)) if updated_participants else None


    async def leave_tournament(self, tournament_id: int, player_uuid: UUID4) -> Tournament | None:
        query = (
            select(
                tournament_table.c.participants
            )
            .where(tournament_table.c.id == tournament_id)
        )
        tournament = await database.fetch_one(query)
        if not tournament:
            return None

        participants = tournament["participants"] or []
        if player_uuid not in participants:
            return None

        participants = [p for p in participants if p != player_uuid]

        updated_query = (
            tournament_table.update()
            .where(tournament_table.c.id == tournament_id)
            .values(participants=participants)
            .returning(tournament_table)
        )
        updated_participants = await database.fetch_one(updated_query)
        return Tournament(**updated_participants) if updated_participants else None

    async def _get_by_id(self, tournament_id: int) -> Record | None:
        query = (
            tournament_table.select()
            .where(tournament_table.c.id == tournament_id)
            .order_by(tournament_table.c.id.asc())
        )
        return await database.fetch_one(query)

    async def get_quiz_by_id(self, quiz_id: int) -> Any | None:
        query = (
            select(
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("quiz_title"),
                quiz_table.c.description.label("quiz_description"),
                quiz_table.c.shared.label("quiz_shared"),
                quiz_table.c.reward.label("quiz_reward"),
                player_table.c.id.label("player_id"),
            )
            .select_from(
                join(
                    player_table,
                    quiz_table,
                    quiz_table.c.player_id == player_table.c.id
                )
            )
            .where(quiz_table.c.id == quiz_id)
            .order_by(quiz_table.c.id.asc())
        )

        quiz = await database.fetch_one(query)
        return QuizDTO.from_record(quiz) if quiz else None