"""Module containing reward service implementation."""

from typing import Iterable
from quizapi.core.domain.history import History
from quizapi.core.domain.reward import Reward, RewardIn
from quizapi.core.repositories.ireward import IRewardRepository
from quizapi.infrastructure.dto.rewarddto import RewardDTO
from quizapi.infrastructure.services.ireward import IRewardService

from pydantic import UUID4

class RewardService(IRewardService):
    """A class implementing the reward service."""

    _repository: IRewardRepository

    def __init__(self, repository: IRewardRepository):
        """The initializer of the `reward service`.

        Args:
            repository (IRewardRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_all_rewards(self) -> Iterable[RewardDTO]:
        """Getting all rewards from the repository.

        Returns:
            Iterable[RewardDTO]: A collection of all rewards.
        """
        return await self._repository.get_all_rewards()

    async def get_reward_by_id(self, reward_id: int) -> RewardDTO | None:
        """Getting a reward by ID.

        Args:
            reward_id (int): The ID of the reward.

        Returns:
            RewardDTO | None: The reward data if found, otherwise None.
        """
        return await self._repository.get_reward_by_id(reward_id)

    async def get_rewards_by_player(self, player_id: UUID4) -> Iterable[RewardDTO]:
        """Getting all rewards assigned to a player.

        Args:
            player_id (UUID4): The UUID of the player.

        Returns:
            Iterable[RewardDTO]: A collection of rewards associated with the player.
        """
        return await self._repository.get_rewards_by_player(player_id)

    async def collect_reward(self, data: RewardIn) -> Reward | None:
        """Collecting a reward for a player if they meet the criteria.

        Args:
            data (RewardIn): The reward data input.

        Returns:
            Reward | None: The collected reward if successful, otherwise None.
        """
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

    async def delete_reward(self, quiz_id: int) -> bool:
        """Removing a reward associated with a quiz.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_reward(quiz_id)

    async def get_histories_by_quiz(self, quiz_id: int, player_id: UUID4) -> Iterable[History] | None:
        """Getting the histories of a player for a given quiz.

        Args:
            quiz_id (int): The ID of the quiz.
            player_id (UUID4): The UUID of the player.

        Returns:
            Iterable[History] | None: A collection of histories if found, otherwise None.
        """
        return await self._repository.get_histories_by_quiz(quiz_id, player_id)

    async def get_reward_by_quiz(self, quiz_id: int) -> str | None:
        """Getting the reward name associated with a quiz.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            str | None: The name of the reward if found, otherwise None.
        """
        return await self._repository.get_reward_by_quiz(quiz_id)