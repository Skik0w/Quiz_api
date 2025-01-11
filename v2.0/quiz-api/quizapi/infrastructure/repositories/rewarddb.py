"""Module containing reward database repository implementation."""

from typing import Any, Iterable
from asyncpg import Record # type: ignore
from sqlalchemy import select
from pydantic import UUID4

from quizapi.core.repositories.ireward import IRewardRepository
from quizapi.core.domain.reward import Reward, RewardIn
from quizapi.core.domain.history import History
from quizapi.db import (
    reward_table,
    history_table,
    quiz_table,
    database,
)
from quizapi.infrastructure.dto.rewarddto import RewardDTO
from sqlalchemy import and_

class RewardRepository(IRewardRepository):
    """A class implementing the reward repository."""
    async def get_all_rewards(self) -> Iterable[Any]:
        """Getting all rewards from the database.

        Returns:
            Iterable[Any]: A collection of all rewards.
        """
        query = (
            select(
                reward_table
            )
            .order_by(
                reward_table.c.id.asc()
            )
        )

        rewards = await database.fetch_all(query)
        return [RewardDTO.from_record(reward) for reward in rewards]

    async def get_reward_by_id(self, reward_id: int) -> Any | None:
        """Getting a reward by ID.

        Args:
            reward_id (int): The ID of the reward.

        Returns:
            Any | None: The reward data if found, otherwise None.
        """
        query = select(
            reward_table
        ).where(
            reward_table.c.id == reward_id
        ).order_by(
            reward_table.c.id.asc()
        )
        reward = await database.fetch_one(query)
        return RewardDTO.from_record(reward) if reward else None

    async def get_rewards_by_player(self, player_id: UUID4) -> Iterable[Any] | None:
        """Getting rewards by player ID.

        Args:
            player_id (UUID4): The UUID of the player.

        Returns:
            Iterable[Any] | None: A collection of rewards belonging to the player.
        """
        query = (
            reward_table.select()
            .where(reward_table.c.player_id == player_id)
        )
        rewards = await database.fetch_all(query)
        return [Reward(**dict(reward)) for reward in rewards]

    async def collect_reward(self, data: RewardIn, reward: str, value: int) -> Any | None:
        """Collecting a reward and storing it in the database.

        Args:
            data (RewardIn): The reward data.
            reward (str): The reward name.
            value (int): The reward value.

        Returns:
            Any | None: The collected reward if successful, otherwise None.
        """
        query = reward_table.insert().values(
            player_id=data.player_id,
            quiz_id=data.quiz_id,
            reward=reward,
            value=value,
        )
        new_reward_id = await database.execute(query)
        new_reward = await self._get_by_id(new_reward_id)
        return Reward(**dict(new_reward)) if new_reward else None

    async def delete_reward(self, reward_id: int) -> bool:
        """Removing a reward from the database.

        Args:
            reward_id (int): The ID of the reward.

        Returns:
            bool: Success of the operation.
        """
        if self._get_by_id(reward_id):
            query = reward_table.delete().where(reward_table.c.id == reward_id)
            await database.execute(query)
            return True
        return False

    async def get_histories_by_quiz(self, quiz_id: int, player_id: UUID4) -> Iterable[Any] | None:
        """Getting histories by quiz ID and player ID.

        Args:
            quiz_id (int): The ID of the quiz.
            player_id (UUID4): The UUID of the player.

        Returns:
            Iterable[Any] | None: A collection of histories related to the quiz and player.
        """
        query = (
            history_table.select()
            .where(and_
                (
                history_table.c.quiz_id == quiz_id,
                history_table.c.player_id == player_id,
            )
            )
        )
        histories = await database.fetch_all(query)
        return [History(**dict(history)) for history in histories]

    async def get_reward_by_quiz(self, quiz_id: int) -> Any | None:
        """Getting a reward by quiz ID.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Any | None: The reward data if found, otherwise None.
        """
        query = (
            select(quiz_table.c.reward)
            .where(quiz_table.c.id == quiz_id)
        )
        reward = await database.fetch_one(query)
        return reward["reward"] if reward else None

    async def _get_by_id(self, reward_id: int) -> Record | None:
        """A private method getting a reward from the database based on its ID.

        Args:
            reward_id (int): The ID of the reward.

        Returns:
            Record | None: The reward record if exists.
        """
        query = (
            reward_table.select()
            .where(reward_table.c.id == reward_id)
            .order_by(reward_table.c.id.asc())
        )
        return await database.fetch_one(query)

