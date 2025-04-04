"""Module containing quiz database repository implementation."""

from typing import Any, Iterable

from asyncpg import Record # type: ignore
from sqlalchemy import select, join

from quizapi.core.repositories.iquiz import IQuizRepository
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.db import (
    quiz_table,
    player_table,
    database,
)
from quizapi.infrastructure.dto.quizdto import QuizDTO

class QuizRepository(IQuizRepository):
    """A class implementing the quiz repository."""

    async def get_all_quizzes(self) -> Iterable[Any]:
        """Getting all quizzes from the database.

        Returns:
            Iterable[Any]: A collection of all quizzes.
        """
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
            .order_by(quiz_table.c.id.asc())
        )

        quizzes = await database.fetch_all(query)
        return [QuizDTO.from_record(quiz) for quiz in quizzes]

    async def get_quiz_by_id(self, quiz_id: int) -> Any | None:
        """Getting a quiz by ID.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Any | None: The quiz data if found, otherwise None.
        """
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
        )

        quiz = await database.fetch_one(query)
        return QuizDTO.from_record(quiz) if quiz else None

    async def add_quiz(self, data: QuizIn) -> Any | None:
        """Adding a new quiz to the database.

        Args:
            data (QuizIn): The quiz data.

        Returns:
            Any | None: The newly created quiz if successful, otherwise None.
        """
        reward = await self.get_quiz_by_reward(data.reward)
        if reward:
            return None
        query = quiz_table.insert().values(**data.model_dump())
        new_quiz_id = await database.execute(query)
        new_quiz = await self._get_by_id(new_quiz_id)
        return Quiz(**dict(new_quiz)) if new_quiz else None

    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn,
    ) -> Any | None:
        """Updating a quiz in the database.

        Args:
            quiz_id (int): The ID of the quiz.
            data (QuizIn): The updated quiz data.

        Returns:
            Any | None: The updated quiz if successful, otherwise None.
        """
        reward = await self.get_quiz_by_reward(data.reward)
        if reward and reward.id != quiz_id:
            return None

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
        """Removing a quiz from the database.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            bool: Success of the operation.
        """
        if self._get_by_id(quiz_id):
            query = quiz_table.delete().where(quiz_table.c.id == quiz_id)
            await database.execute(query)
            return True
        return False

    async def share_quiz(self, quiz_id: int) -> Any | None:
        """Sharing a quiz by setting its shared attribute to True.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Any | None: The updated quiz if successful, otherwise None.
        """
        query = (
            quiz_table.update()
            .where(quiz_table.c.id == quiz_id)
            .values(shared=True)
        )
        await database.execute(query)
        return await self._get_by_id(quiz_id)

    async def get_quiz_by_reward(self, reward: str) -> Any | None:
        """Getting a quiz by its reward name.

        Args:
            reward (str): The reward associated with the quiz.

        Returns:
            Any | None: The quiz data if found, otherwise None.
        """
        query = (
            select(
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("quiz_title"),
                quiz_table.c.description.label("quiz_description"),
                quiz_table.c.shared.label("quiz_shared"),
                quiz_table.c.reward.label("quiz_reward"),
                player_table.c.id.label("player_id"),
            )
            .where(quiz_table.c.reward == reward)
        )
        quiz = await database.fetch_one(query)
        return QuizDTO.from_record(quiz) if quiz else None

    async def _get_by_id(self, quiz_id: int) -> Record | None:
        """A private method getting a quiz from the database based on its ID.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Record | None: The quiz record if exists.
        """
        query = (
            quiz_table.select()
            .where(quiz_table.c.id == quiz_id)
            .order_by(quiz_table.c.id.asc())
        )
        return await database.fetch_one(query)

