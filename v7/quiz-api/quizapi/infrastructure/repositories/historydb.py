from typing import Any, Iterable
from asyncpg import Record # type: ignore
from sqlalchemy import select, join, cast, Integer

from quizapi.core.domain.question import Question
from quizapi.core.repositories.ihistory import IHistoryRepository
from quizapi.core.domain.history import History, HistoryIn
from quizapi.db import (
    quiz_table,
    player_table,
    history_table,
    question_table,
    database,
)
from quizapi.infrastructure.dto.historydto import HistoryDTO

class HistoryRepository(IHistoryRepository):

    async def get_all_histories(self) -> Iterable[Any]:
        query = (
            select(
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("title"),
                quiz_table.c.description.label("description"),
                player_table.c.id.label("player_id1"),
                player_table.c.username.label("player_username1"),
                player_table.c.id.label("player_id2"),
                player_table.c.username.label("player_username2"),
                history_table.c.id.label("id"),
                history_table.c.total_questions,
                history_table.c.correct_answers,
                history_table.c.effectiveness,
                history_table.c.timestamp,
            )
            .select_from(
                join(
                    join(
                        history_table,
                        player_table,
                        cast(history_table.c.player_id, Integer) == cast(player_table.c.id, Integer)
                    ),
                    quiz_table,
                    cast(history_table.c.quiz_id, Integer) == cast(quiz_table.c.id, Integer)
                )
            )
            .order_by(history_table.c.id.asc())
        )

        histories = await database.fetch_all(query)
        return [HistoryDTO.from_record(history) for history in histories]

    async def get_history_by_id(self, history_id: int) -> Any | None:
        query = (
            select(
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("title"),
                quiz_table.c.description.label("description"),
                player_table.c.id.label("player_id1"),
                player_table.c.username.label("player_username1"),
                player_table.c.id.label("player_id2"),
                player_table.c.username.label("player_username2"),
                history_table.c.id.label("id"),
                history_table.c.total_questions,
                history_table.c.correct_answers,
                history_table.c.effectiveness,
                history_table.c.timestamp,
            )
            .select_from(
                join(
                    join(
                        history_table,
                        player_table,
                        cast(history_table.c.player_id, Integer) == cast(player_table.c.id, Integer)
                    ),
                    quiz_table,
                    cast(history_table.c.quiz_id, Integer) == cast(quiz_table.c.id, Integer)
                )
            )
            .where(cast(history_table.c.id, Integer) == history_id)
            .order_by(history_table.c.id.asc())
        )

        history = await database.fetch_one(query)
        return HistoryDTO.from_record(history) if history else None

    async def get_history_by_player(self, player_id: int) -> Iterable[Any] | None:

        query = (
            history_table.select()
            .where(history_table.c.player_id == player_id)
        )
        histories = await database.fetch_all(query)
        return [History(**dict(history)) for history in histories]

    async def add_history(self, data: HistoryIn) -> Any | None:
        query = history_table.insert().values(**data.model_dump())
        new_history_id = await database.execute(query)
        new_history = await self._get_by_id(new_history_id)
        return History(**dict(new_history)) if new_history else None

    async def update_history(
            self,
            history_id: int,
            data: HistoryIn,
    ) -> Any | None:

        if self._get_by_id(history_id):
            query = (
                history_table.update()
                .where(history_table.c.id == history_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            history = await self._get_by_id(history_id)
            return History(**dict(history)) if history else None
        return None

    async def delete_history(self, history_id: int) -> bool:
        if self._get_by_id(history_id):
            query = history_table.delete().where(history_table.c.id == history_id)
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, history_id: int) -> Record | None:
        query = (
            history_table.select()
            .where(history_table.c.id == history_id)
            .order_by(history_table.c.id.asc())
        )
        return await database.fetch_one(query)

    async def get_total_questions_by_quiz(self, quiz_id: int) -> Iterable[Any] | None:
        query = (
            question_table.select()
            .where(question_table.c.quiz_id == quiz_id)
        )
        questions = await database.fetch_all(query)
        return [Question(**dict(question)) for question in questions]