from typing import Any, Iterable

from asyncpg import Record # type: ignore
from sqlalchemy import select, join
from pydantic import UUID4

from quizapi.core.repositories.ireward import IRewardRepository
from quizapi.core.domain.reward import Reward, RewardIn
from quizapi.core.domain.history import History
from quizapi.db import (
    reward_table,
    history_table,
    quiz_table,
    player_table,
    database,
)
from quizapi.infrastructure.dto.rewarddto import RewardDTO
from quizapi.infrastructure.dto.historydto import HistoryDTO
from sqlalchemy import and_

class RewardRepository(IRewardRepository):

    async def get_all_rewards(self) -> Iterable[Any]:
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
        query = (
            reward_table.select()
            .where(reward_table.c.player_id == player_id)
        )
        rewards = await database.fetch_all(query)
        return [Reward(**dict(reward)) for reward in rewards]

    async def collect_reward(self, data: RewardIn, reward: str, value: int) -> Any | None:

        query = reward_table.insert().values(
            player_id=data.player_id,
            quiz_id=data.quiz_id,
            reward=reward,
            value=value,
        )
        new_reward_id = await database.execute(query)
        new_reward = await self._get_by_id(new_reward_id)
        return Reward(**dict(new_reward)) if new_reward else None


    async def update_reward(
            self,
            reward_id: int,
            data: RewardIn,
    ) -> Any | None:

        if self._get_by_id(reward_id):
            query = (
                reward_table.update()
                .where(reward_table.c.id == reward_id)
                .values(**data.model_dump())
            )
            await database.execute(query)
            reward = await self._get_by_id(reward_id)
            return Reward(**dict(reward)) if reward else None
        return None

    async def delete_reward(self, reward_id: int) -> bool:
        if self._get_by_id(reward_id):
            query = reward_table.delete().where(reward_table.c.id == reward_id)
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, reward_id: int) -> Record | None:
        query = (
            reward_table.select()
            .where(reward_table.c.id == reward_id)
            .order_by(reward_table.c.id.asc())
        )
        return await database.fetch_one(query)

    async def get_histories_by_quiz(self, quiz_id: int, player_id: UUID4) -> Iterable[Any] | None:
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
        query = (
            select(quiz_table.c.reward)
            .where(quiz_table.c.id == quiz_id) #było c.quiz_id
        )
        reward = await database.fetch_one(query)
        return reward["reward"] if reward else None

