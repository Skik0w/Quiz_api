from abc import ABC, abstractmethod
from typing import Any, Iterable
from quizapi.core.domain.reward import RewardIn

from pydantic import UUID4

class IRewardRepository(ABC):

    @abstractmethod
    async def get_all_rewards(self) -> Iterable[Any]:
        """ """

    @abstractmethod
    async def get_reward_by_id(self, reward_id: int) -> Any | None:
        """ """

    async def get_rewards_by_player(self, player_id: UUID4) -> Iterable[Any]:
        """ """

    @abstractmethod
    async def collect_reward(self, data: RewardIn, reward: str) -> Any | None:
        """ """

    @abstractmethod
    async def update_reward(
            self,
            reward_id: int,
            data: RewardIn
    ) -> Any | None:
        """ """

    @abstractmethod
    async def delete_reward(self, quiz_id: int) -> bool:
        """ """

    async def get_histories_by_quiz(self, quiz_id: int, player_id: UUID4) -> Iterable[Any] | None:
        """ """

    async def get_reward_by_quiz(self, quiz_id: int) -> Any | None:
        """ """