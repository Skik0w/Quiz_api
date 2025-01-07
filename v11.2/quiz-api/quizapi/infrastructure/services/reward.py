from typing import Iterable


from quizapi.core.domain.history import History
from quizapi.core.domain.reward import Reward, RewardIn
from quizapi.core.repositories.ireward import IRewardRepository
from quizapi.infrastructure.dto.rewarddto import RewardDTO
from quizapi.infrastructure.services.ireward import IRewardService

from pydantic import UUID4

class RewardService(IRewardService):

    _repository: IRewardRepository

    def __init__(self, repository: IRewardRepository):

        self._repository = repository

    async def get_all_rewards(self) -> Iterable[RewardDTO]:
        return await self._repository.get_all_rewards()

    async def get_reward_by_id(self, reward_id: int) -> RewardDTO | None:
        return await self._repository.get_reward_by_id(reward_id)

    async def get_rewards_by_player(self, player_id: UUID4) -> Iterable[RewardDTO]:
        return await self._repository.get_rewards_by_player(player_id)

    async def collect_reward(self, data: RewardIn) -> Reward | None:
        histories = await self._repository.get_histories_by_quiz(data.quiz_id, data.player_id)
        if not histories:
            return None

        for history in histories:
            if history.effectiveness >= 0.75:
                name = await self._repository.get_reward_by_quiz(history.quiz_id)
                value = history.total_questions * 10
                return await self._repository.collect_reward(
                    data=data,
                    reward=name,
                    value=value,
                )
        return None


    async def update_reward(
            self,
            reward_id: int,
            data: RewardIn
    ) -> Reward | None:
        return await self._repository.update_reward(
            reward_id=reward_id,
            data=data,
        )

    async def delete_reward(self, quiz_id: int) -> bool:
        return await self._repository.delete_reward(quiz_id)

    async def get_histories_by_quiz(self, quiz_id: int, player_id: UUID4) -> Iterable[History] | None:
        return await self._repository.get_histories_by_quiz(quiz_id, player_id)

    async def get_reward_by_quiz(self, quiz_id: int) -> str | None:
        return await self._repository.get_reward_by_quiz(quiz_id)