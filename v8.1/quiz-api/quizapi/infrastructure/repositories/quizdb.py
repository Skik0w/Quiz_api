from typing import Any, Iterable
from sqlalchemy.dialects.postgresql import UUID

from asyncpg import Record # type: ignore
from sqlalchemy import select, join, cast, Integer

from quizapi.core.repositories.iquiz import IQuizRepository
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.db import (
    quiz_table,
    player_table,
    database,
)
from quizapi.infrastructure.dto.quizdto import QuizDTO

class QuizRepository(IQuizRepository):

    async def get_all_quizzes(self) -> Iterable[Any]:
        query = (
            select(
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("quiz_title"),
                quiz_table.c.description.label("quiz_description"),
                quiz_table.c.shared.label("quiz_shared"),
                player_table.c.id.label("player_id"),
                player_table.c.username.label("player_username"),
            )
            .select_from(
                join(
                    player_table,
                    quiz_table,
                    cast(quiz_table.c.player_id, UUID) == player_table.c.id
                )
            )
            .order_by(quiz_table.c.id.asc())
        )

        quizzes = await database.fetch_all(query)
        return [QuizDTO.from_record(quiz) for quiz in quizzes]

    async def get_quiz_by_id(self, quiz_id: int) -> Any | None:
        query = (
            select(
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("quiz_title"),
                quiz_table.c.description.label("quiz_description"),
                quiz_table.c.shared.label("quiz_shared"),
                player_table.c.id.label("player_id"),
                player_table.c.username.label("player_username"),
            )
            .select_from(
                join(
                    player_table,
                    quiz_table,
                    cast(quiz_table.c.player_id, UUID) == player_table.c.id
                )
            )
            .where(cast(quiz_table.c.id, Integer) == quiz_id)
            .order_by(quiz_table.c.id.asc())
        )

        quiz = await database.fetch_one(query)
        return QuizDTO.from_record(quiz) if quiz else None

    async def add_quiz(self, data: QuizIn) -> Any | None:
        query = quiz_table.insert().values(**data.model_dump())
        new_quiz_id = await database.execute(query)
        new_quiz = await self._get_by_id(new_quiz_id)
        return Quiz(**dict(new_quiz)) if new_quiz else None

    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn,
    ) -> Any | None:

        if self._get_by_id(quiz_id):
            query = (
                quiz_table.update()
                .where(quiz_table.c.id == quiz_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            quiz = await self._get_by_id(quiz_id)
            return Quiz(**dict(quiz)) if quiz else None
        return None

    async def delete_quiz(self, quiz_id: int) -> bool:
        if self._get_by_id(quiz_id):
            query = quiz_table.delete().where(quiz_table.c.id == quiz_id)
            await database.execute(query)
            return True
        return False

    async def share_quiz(self, quiz_id: int) -> Any | None:
        query = (
            quiz_table.update()
            .where(quiz_table.c.id == quiz_id)
            .values(shared=True)
        )
        await database.execute(query)
        return await self._get_by_id(quiz_id)

    async def _get_by_id(self, quiz_id: int) -> Record | None:

        query = (
            quiz_table.select()
            .where(quiz_table.c.id == quiz_id)
            .order_by(quiz_table.c.id.asc())
        )
        return await database.fetch_one(query)

