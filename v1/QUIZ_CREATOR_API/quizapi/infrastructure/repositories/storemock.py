from typing import Iterable
from quizapi.core.domain.store import Reward, RewardIn
from quizapi.core.repositories.istore import IStoreRepository
from quizapi.infrastructure.repositories.db import rewards

class StoreMockRepository(IStoreRepository):

    async def get_reward_by_id(self, reward_id: int) -> Reward | None:
        return next(
            (obj for obj in rewards if obj.id == reward_id), None
        )

    async def get_all_rewards(self) -> Iterable[Reward]:
        return rewards

    async def add_reward(self, reward: RewardIn) -> None:
        rewards.append(reward)

    async def delete_reward(self, reward_id: int) -> bool:
        if reward_pos := \
                next(filter(lambda r: r.id == reward_id, rewards)):
            rewards.remove(reward_pos)
            return True