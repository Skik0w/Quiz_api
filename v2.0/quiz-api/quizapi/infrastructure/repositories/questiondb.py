"""Module containing question database repository implementation."""

from typing import Any, Iterable
from asyncpg import Record # type: ignore
from sqlalchemy import select, join

from quizapi.core.repositories.iquestion import IQuestionRepository
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.db import question_table, database, quiz_table, player_table
from quizapi.infrastructure.dto.questiondto import QuestionDTO

class QuestionRepository(IQuestionRepository):
    """A class implementing the question repository."""

    async def get_all_questions(self) -> Iterable[Any]:
        """Getting all questions from the database.

        Returns:
            Iterable[Any]: A collection of all questions.
        """
        query = (
            select(
                question_table.c.id.label("id"),
                question_table.c.question_text.label("question_text"),
                question_table.c.option_one.label("option_one"),
                question_table.c.option_two.label("option_two"),
                question_table.c.option_three.label("option_three"),
                question_table.c.option_four.label("option_four"),
                question_table.c.correct_option.label("correct_option"),
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("title"),
                quiz_table.c.description.label("description"),
                quiz_table.c.shared.label("shared"),
                quiz_table.c.reward.label("reward"),
                player_table.c.id.label("player_id"),
            )
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
        """Getting a question by ID.

        Args:
            question_id (int): The ID of the question.

        Returns:
            Record | None: The question record if found, otherwise None.
        """
        query = (
            select(
                question_table.c.id.label("id"),
                question_table.c.question_text.label("question_text"),
                question_table.c.option_one.label("option_one"),
                question_table.c.option_two.label("option_two"),
                question_table.c.option_three.label("option_three"),
                question_table.c.option_four.label("option_four"),
                question_table.c.correct_option.label("correct_option"),
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("title"),
                quiz_table.c.description.label("description"),
                quiz_table.c.shared.label("shared"),
                quiz_table.c.reward.label("reward"),
                player_table.c.id.label("player_id"),
            )
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
            .where(question_table.c.id == question_id)
            .order_by(question_table.c.id.asc())
        )
        question = await database.fetch_one(query)
        return QuestionDTO.from_record(question) if question else None

    async def get_questions_by_quiz(self, quiz_id: int) -> Iterable[Any] | None:
        """Getting questions by quiz ID.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Iterable[Any] | None: A collection of questions for the quiz.
        """
        query = (
            question_table.select()
            .where(question_table.c.quiz_id == quiz_id)
        )
        questions = await database.fetch_all(query)
        return [Question(**dict(question)) for question in questions]

    async def add_question(self, data: QuestionIn) -> Any | None:
        """Adding a new question to the database.

        Args:
            data (QuestionIn): The question data.

        Returns:
            Any | None: The newly created question if successful, otherwise None.
        """
        query = question_table.insert().values(**data.model_dump())
        new_question_id = await database.execute(query)
        new_question = await self._get_by_id(new_question_id)
        return Question(**dict(new_question)) if new_question else None

    async def update_question(
            self,
            question_id: int,
            data: QuestionIn,
    ) -> Any | None:
        """Updating a question in the database.

        Args:
            question_id (int): The ID of the question.
            data (QuestionIn): The updated question data.

        Returns:
            Any | None: The updated question if successful, otherwise None.
        """
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
        """Removing a question from the database.

        Args:
            question_id (int): The ID of the question.

        Returns:
            bool: Success of the operation.
        """
        if self._get_by_id(question_id):
            query = question_table.delete().where(question_table.c.id == question_id)
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, question_id: int) -> Record | None:
        """A private method getting a question from the database based on its ID.

        Args:
            question_id (int): The ID of the question.

        Returns:
            Record | None: The question record if exists.
        """
        query = (
            question_table.select()
            .where(question_table.c.id == question_id)
            .order_by(question_table.c.id.asc())
        )
        return await database.fetch_one(query)