"""Module containing history database repository implementation."""

from typing import Any, Iterable
from asyncpg import Record # type: ignore
from sqlalchemy import select, join
from pydantic import UUID4

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
    """A class implementing the history repository."""

    async def get_all_histories(self) -> Iterable[Any]:
        """Getting all history records from the database.

            Returns:
                Iterable[Any]: A collection of all history records.
        """
        query = (
            select(
                history_table.c.id.label("id"),
                history_table.c.total_questions.label("total_questions"),
                history_table.c.correct_answers.label("correct_answers"),
                history_table.c.effectiveness.label("effectiveness"),
                history_table.c.timestamp.label("timestamp"),
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("title"),
                quiz_table.c.description.label("description"),
                quiz_table.c.shared.label("shared"),
                quiz_table.c.reward.label("reward"),
                history_table.c.player_id.label("player_id"),
                quiz_table.c.player_id.label("player_id_2"),
            )
            .select_from(
                join(
                    history_table,
                    join(
                        quiz_table,
                        player_table,
                        quiz_table.c.player_id == player_table.c.id
                    ),
                    history_table.c.quiz_id == quiz_table.c.id
                )
            )
            .order_by(history_table.c.id.asc())
        )

        histories = await database.fetch_all(query)
        return [HistoryDTO.from_record(history) for history in histories]

    async def get_history_by_id(self, history_id: int) -> Any | None:
        """Getting a specific history record by ID.

        Args:
            history_id (int): The ID of the history record.

        Returns:
            Any | None: The history record if found, otherwise None.
        """
        query = (
            select(
                history_table.c.id.label("id"),
                history_table.c.total_questions.label("total_questions"),
                history_table.c.correct_answers.label("correct_answers"),
                history_table.c.effectiveness.label("effectiveness"),
                history_table.c.timestamp.label("timestamp"),
                quiz_table.c.id.label("quiz_id"),
                quiz_table.c.title.label("title"),
                quiz_table.c.description.label("description"),
                quiz_table.c.shared.label("shared"),
                quiz_table.c.reward.label("reward"),
                history_table.c.player_id.label("player_id"),
                quiz_table.c.player_id.label("player_id_2"),
            )
            .select_from(
                join(
                    history_table,
                    join(
                        quiz_table,
                        player_table,
                        quiz_table.c.player_id == player_table.c.id
                    ),
                    history_table.c.quiz_id == quiz_table.c.id
                )
            )
            .where(history_table.c.id == history_id)
            .order_by(history_table.c.id.asc())
        )

        history = await database.fetch_one(query)
        return HistoryDTO.from_record(history) if history else None

    async def get_history_by_player(self, player_id: UUID4) -> Iterable[Any] | None:
        """Getting all history records for a given player.

        Args:
            player_id (UUID4): The ID of the player.

        Returns:
            Iterable[Any] | None: A collection of history records for the player.
        """
        query = (
            history_table.select()
            .where(history_table.c.player_id == player_id)
        )
        histories = await database.fetch_all(query)
        return [History(**dict(history)) for history in histories]

    async def add_history(self, data: HistoryIn, total_questions: int, effectiveness: float) -> Any | None:
        """Adding a new history record to the database.

        Args:
            data (HistoryIn): The history data.
            total_questions (int): The total number of questions.
            effectiveness (float): The effectiveness score.

        Returns:
            Any | None: The newly created history record.
        """
        query = history_table.insert().values(
            player_id=data.player_id,
            quiz_id=data.quiz_id,
            correct_answers=data.correct_answers,
            timestamp=data.timestamp,
            total_questions=total_questions,
            effectiveness=effectiveness
        )
        new_history_id = await database.execute(query)
        new_history = await self._get_by_id(new_history_id)
        return History(**dict(new_history)) if new_history else None

    async def update_history(
            self,
            history_id: int,
            data: HistoryIn,
            total_questions: int,
            effectiveness: float
    ) -> History | None:
        """Updating an existing history record in the database.

        Args:
            history_id (int): The ID of the history record.
            data (HistoryIn): The updated history data.
            total_questions (int): The total number of questions.
            effectiveness (float): The effectiveness score.

        Returns:
            History | None: The updated history record if successful, otherwise None.
        """
        existing_history = await self._get_by_id(history_id)
        if not existing_history:
            return None

        query = (
            history_table.update()
            .where(history_table.c.id == history_id)
            .values(
                player_id=data.player_id,
                quiz_id=data.quiz_id,
                correct_answers=data.correct_answers,
                timestamp=data.timestamp,
                total_questions=total_questions,
                effectiveness=effectiveness,
            )
        )
        await database.execute(query)
        updated_history = await self._get_by_id(history_id)
        return History(**dict(updated_history)) if updated_history else None

    async def delete_history(self, history_id: int) -> bool:
        """Deleting a history record from the database.

        Args:
            history_id (int): The ID of the history record to be deleted.

        Returns:
            bool: True if deleted successfully, otherwise False.
        """
        if self._get_by_id(history_id):
            query = history_table.delete().where(history_table.c.id == history_id)
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, history_id: int) -> Record | None:
        """Getting a history record by ID from the database.

        Args:
            history_id (int): The ID of the history record.

        Returns:
            Record | None: The history record if found.
        """
        query = (
            history_table.select()
            .where(history_table.c.id == history_id)
            .order_by(history_table.c.id.asc())
        )
        return await database.fetch_one(query)

    async def get_total_questions_by_quiz(self, quiz_id: int) -> Iterable[Any] | None:
        """Getting all questions related to a specific quiz.

            Args:
                quiz_id (int): The ID of the quiz.

            Returns:
                Iterable[Any] | None: A collection of questions associated with the quiz.
        """
        query = (
            question_table.select()
            .where(question_table.c.quiz_id == quiz_id)
        )
        questions = await database.fetch_all(query)
        return [Question(**dict(question)) for question in questions]