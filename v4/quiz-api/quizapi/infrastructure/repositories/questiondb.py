from typing import Any, Iterable
from asyncpg import Record # type: ignore
from sqlalchemy import select, join
from quizapi.core.repositories.iquestion import IQuestionRepository
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.db import question_table, database, quiz_table, player_table
from quizapi.infrastructure.dto.questiondto import QuestionDTO

class QuestionRepository(IQuestionRepository):

    async def get_all_questions(self) -> Iterable[Any]:
        query = select(
            question_table, quiz_table, player_table
            .select_from(
                join(
                    question_table,
                    join(
                        quiz_table,
                        player_table,
                        quiz_table.c.player_id == player_table.c.id
                    ),
                    question_table.c.quiz_id == quiz_table.c.id
                )
            )
            .order_by(question_table.c.id.asc())
        )
        questions = await database.fetch_all(query)
        return [QuestionDTO.from_record(question) for question in questions]

    async def get_question_by_id(self, question_id: int) -> Record | None:
        question = await self._get_by_id(question_id)
        return Question(**dict(question)) if question else None

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
            query = question_table.update().where(question_table.c.id == question_id).values(**data.model_dump())
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
        query = question_table.select().where(question_table.c.id == question_id).order_by(question_table.c.id.asc())
        return await database.fetch_one(query)

