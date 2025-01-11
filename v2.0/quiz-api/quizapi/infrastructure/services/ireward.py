"""Module containing reward service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from quizapi.core.domain.history import History
from quizapi.core.domain.reward import Reward, RewardIn
from quizapi.infrastructure.dto.rewarddto import RewardDTO

from pydantic import UUID4

class IRewardService(ABC):
    """An abstract class representing protocol of reward service."""
    @abstractmethod
    async def get_all_rewards(self) -> Iterable[RewardDTO]:
        """The abstract getting all rewards from the repository.

        Returns:
            Iterable[RewardDTO]: The collection of all rewards.
        """
    @abstractmethod
    async def get_reward_by_id(self, reward_id: int) -> RewardDTO | None:
        """The abstract getting a reward by ID from the repository.

        Args:
            reward_id (int): The ID of the reward.

        Returns:
            RewardDTO | None: The reward data if exists.
        """

    async def get_rewards_by_player(self, player_id: UUID4) -> Iterable[RewardDTO]:
        """The abstract getting rewards associated with a player.

        Args:
            player_id (UUID4): The UUID of the player.

        Returns:
            Iterable[RewardDTO]: A collection of rewards associated with the player.
        """

    @abstractmethod
    async def collect_reward(self, data: RewardIn) -> Reward | None:
        """The abstract collecting a reward based on quiz performance.

        Args:
            data (RewardIn): The reward collection request data.

        Returns:
            Reward | None: The collected reward if successful.
        """

    @abstractmethod
    async def delete_reward(self, quiz_id: int) -> bool:
        """The abstract removing a reward from the repository.

         Args:
             quiz_id (int): The ID of the quiz associated with the reward.

         Returns:
             bool: Success of the operation.
         """

    @abstractmethod
    async def get_histories_by_quiz(self, quiz_id: int, player_id: UUID4) -> Iterable[History] | None:
        """The abstract getting all history records for a player in a given quiz.

        Args:
            quiz_id (int): The ID of the quiz.
            player_id (UUID4): The UUID of the player.

        Returns:
            Iterable[History] | None: A collection of history records for the given quiz and player.
        """

    @abstractmethod
    async def get_reward_by_quiz(self, quiz_id: int) -> str | None:
        """The abstract getting the reward name associated with a quiz.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            str | None: The reward name if exists.
        """