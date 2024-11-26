from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.store import Reward, RewardIn

class IStoreService(ABC):

    @abstractmethod
    async def get_reward_by_id(self, reward_id: int) -> Reward | None:
        """ """

    @abstractmethod
    async def get_all_rewards(self) -> Iterable[Reward]:
        """ """

    @abstractmethod
    async def add_reward(self, reward: RewardIn) -> None:
        """ """

    @abstractmethod
    async def delete_reward(self, reward_id: int) -> bool:
        """ """