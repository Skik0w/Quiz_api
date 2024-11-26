"""Module containing store repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from quizapi.core.domain.store import Reward, RewardIn

class IStoreRepository(ABC):

    @abstractmethod
    async def get_reward_by_id(self, reward_id: int) -> Reward | None:
        """The abstract getting a store item by id from the data storage.

        Args:
            reward_id (int): The id of the store item.

        Returns:
            Reward | None: The store item data if exists.
        """

    @abstractmethod
    async def get_all_rewards(self) -> Iterable[Reward]:
        """The abstract getting all store items from the data storage.

        Returns:
            Iterable[Reward]: The collection of all store items.
        """

    @abstractmethod
    async def add_reward(self, reward: RewardIn) -> None:
        """The abstract adding a new store item to the data storage.

        Args:
            reward (Reward): The attributes of the store item.
        """

    @abstractmethod
    async def delete_reward(self, reward_id: int) -> bool:
        """The abstract removing a store item from the data storage.

        Args:
            reward_id (int): The ID of the store item.

        Returns:
            bool: Success of the operation.
        """