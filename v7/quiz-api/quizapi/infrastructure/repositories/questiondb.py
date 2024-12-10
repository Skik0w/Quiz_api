from typing import Any, Iterable
from asyncpg import Record # type: ignore
from sqlalchemy import select, join, cast, Integer
from quizapi.core.repositories.iquestion import IQuestionRepository
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.db import question_table, database, quiz_table, player_table
from quizapi.infrastructure.dto.questiondto import QuestionDTO

class QuestionRepository(IQuestionRepository):

    async def get_all_questions(self) -> Iterable[Any]:
        query = (
            select(
                question_table.c.id.label("id"),
                question_table.c.text.label("text"),
                question_table.c.option_one.label("option_one"),
                question_table.c.option_two.label("option_two"),
                question_table.c.option_three.label("option_three"),
                question_table.c.option_four.label("option_four"),
                question_table.c.correct_answer.label("correct_answer"),
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("title"),
                quiz_table.c.description.label("description"),
                quiz_table.c.shared.label("shared"),
                player_table.c.id.label("player_id"),
                player_table.c.username.label("username")
            )
            .select_from(
                join(
                    question_table,
                    join(
                        quiz_table,
                        player_table,
                        cast(quiz_table.c.player_id, Integer) == cast(player_table.c.id, Integer)
                    ),
                    cast(question_table.c.quiz_id, Integer) == cast(quiz_table.c.id, Integer)
                )
            )
            .order_by(question_table.c.id.asc())
        )
        questions = await database.fetch_all(query)
        return [QuestionDTO.from_record(question) for question in questions]

    async def get_question_by_id(self, question_id: int) -> Record | None:
        query = (
            select(
                question_table.c.id.label("id"),
                question_table.c.text.label("text"),
                question_table.c.option_one.label("option_one"),
                question_table.c.option_two.label("option_two"),
                question_table.c.option_three.label("option_three"),
                question_table.c.option_four.label("option_four"),
                question_table.c.correct_answer.label("correct_answer"),
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("title"),
                quiz_table.c.description.label("description"),
                quiz_table.c.shared.label("shared"),
                player_table.c.id.label("player_id"),
                player_table.c.username.label("username")
            )
            .select_from(
                join(
                    question_table,
                    join(
                        quiz_table,
                        player_table,
                        cast(quiz_table.c.player_id, Integer) == cast(player_table.c.id, Integer)
                    ),
                    cast(question_table.c.quiz_id, Integer) == cast(quiz_table.c.id, Integer)
                )
            )
            .where(cast(question_table.c.id, Integer) == question_id)
            .order_by(question_table.c.id.asc())
        )
        question = await database.fetch_one(query)
        return QuestionDTO.from_record(question) if question else None

    async def get_questions_by_quiz(self, quiz_id: int) -> Iterable[Any] | None:
        query = (
            question_table.select()
            .where(question_table.c.quiz_id == quiz_id)
        )
        questions = await database.fetch_all(query)
        return [Question(**dict(question)) for question in questions]

    async def add_question(self, data: QuestionIn) -> Any | None:
        query = question_table.insert().values(**data.model_dump())
        new_question_id = await database.execute(query)
        new_question = await self._get_by_id(new_question_id)
        return Question(**dict(new_question)) if new_question else None

    async def update_question(
            self,
            question_id: int,
            data: QuestionIn,
    ) -> Any | None:
        if self._get_by_id(question_id):
            query = (
                question_table.update()
                .where(question_table.c.id == question_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            question = await self._get_by_id(question_id)
            return Question(**dict(question)) if question else None
        return None

    async def delete_question(self, question_id: int) -> bool:
        if self._get_by_id(question_id):
            query = question_table.delete().where(question_table.c.id == question_id)
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, question_id: int) -> Record | None:
        query = (
            question_table.select()
            .where(question_table.c.id == question_id)
            .order_by(question_table.c.id.asc())
        )
        return await database.fetch_one(query)