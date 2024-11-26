from typing import Iterable
from quizapi.core.domain.store import Reward, RewardIn
from quizapi.core.repositories.istore import IStoreRepository
from quizapi.infrastructure.services.istore import IStoreService

class StoreService(IStoreService):

    _repository: IStoreRepository

    def __init__(self, repository: IStoreRepository):

        self._repository = repository


    async def get_reward_by_id(self, reward_id: int) -> Reward | None:
        return await self._repository.get_reward_by_id(reward_id)

    async def get_all_rewards(self) -> Iterable[Reward]:
        return await self._repository.get_all_rewards()

    async def add_reward(self, reward: RewardIn) -> None:
        await self._repository.add_reward(reward)

    async def delete_reward(self, reward_id: int) -> bool:
        return await self._repository.delete_reward(reward_id)