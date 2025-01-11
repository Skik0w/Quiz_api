"""Module containing reward repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable
from quizapi.core.domain.reward import RewardIn

from pydantic import UUID4

class IRewardRepository(ABC):
    """An abstract class representing protocol of reward repository."""

    @abstractmethod
    async def get_all_rewards(self) -> Iterable[Any]:
        """The abstract getting all rewards from the data storage.

        Returns:
            Iterable[Any]: The collection of all rewards.
        """

    @abstractmethod
    async def get_reward_by_id(self, reward_id: int) -> Any | None:
        """The abstract getting a reward by ID from the data storage.

         Args:
             reward_id (int): The ID of the reward.

         Returns:
             Any | None: The reward data if exists.
         """

    async def get_rewards_by_player(self, player_id: UUID4) -> Iterable[Any]:
        """The abstract getting rewards by player from the data storage.

        Args:
            player_id (UUID4): The ID of the player.

        Returns:
            Iterable[Any]: The collection of rewards for the given player.
        """

    @abstractmethod
    async def collect_reward(self, data: RewardIn, reward: str, value: int) -> Any | None:
        """The abstract collecting a reward from the data storage.

        Args:
            data (RewardIn): The attributes of the reward.
            reward (str): The reward name.
            value (int): The value associated with the reward.

        Returns:
            Any | None: The collected reward if successful.
        """

    @abstractmethod
    async def delete_reward(self, quiz_id: int) -> bool:
        """The abstract removing a reward from the data storage.

        Args:
            quiz_id (int): The ID of the quiz associated with the reward.

        Returns:
            bool: Success of the operation.
        """

    async def get_histories_by_quiz(self, quiz_id: int, player_id: UUID4) -> Iterable[Any] | None:
        """The abstract getting histories by quiz and player from the data storage.

        Args:
            quiz_id (int): The ID of the quiz.
            player_id (UUID4): The ID of the player.

        Returns:
            Iterable[Any] | None: The collection of histories associated with the quiz and player.
        """

    async def get_reward_by_quiz(self, quiz_id: int) -> Any | None:
        """The abstract getting a reward by quiz from the data storage.

        Args:
            quiz_id (int): The ID of the quiz.

        Returns:
            Any | None: The reward data if exists.
        """