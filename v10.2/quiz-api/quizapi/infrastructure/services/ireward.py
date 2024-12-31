from abc import ABC, abstractmethod
from typing import Iterable

from quizapi.core.domain.history import History
from quizapi.core.domain.reward import Reward, RewardIn
from quizapi.infrastructure.dto.rewarddto import RewardDTO

from pydantic import UUID4

class IRewardService(ABC):

    @abstractmethod
    async def get_all_rewards(self) -> Iterable[RewardDTO]:
        """ """

    @abstractmethod
    async def get_reward_by_id(self, reward_id: int) -> RewardDTO | None:
        """ """

    async def get_rewards_by_player(self, player_id: UUID4) -> Iterable[RewardDTO]:
        """ """

    @abstractmethod
    async def collect_reward(self, data: RewardIn) -> Reward | None:
        """ """

    @abstractmethod
    async def update_reward(
            self,
            reward_id: int,
            data: RewardIn
    ) -> Reward | None:
        """ """

    @abstractmethod
    async def delete_reward(self, quiz_id: int) -> bool:
        """ """

    @abstractmethod
    async def get_histories_by_quiz(self, quiz_id: int, player_id: UUID4) -> Iterable[History] | None:
        """ """

    @abstractmethod
    async def get_reward_by_quiz(self, quiz_id: int) -> str | None:
        """ """