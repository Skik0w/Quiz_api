"""Module containing shop repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4

class IShopRepository(ABC):
    """An abstract class representing protocol of shop repository."""

    @abstractmethod
    async def get_all_items(self) -> Iterable[Any]:
        """The abstract getting all items from the data storage.

        Returns:
            Iterable[Any]: The collection of all items.
        """

    @abstractmethod
    async def sell_item(self, reward_id: int, player_id: UUID4) -> Any | None:
        """The abstract selling an item in the shop.

        Args:
            reward_id (int): The ID of the reward to be sold.
            player_id (UUID4): The ID of the player selling the item.

        Returns:
            Any | None: The sold item data if successful.
        """

    @abstractmethod
    async def buy_item(self, item_id: int, player_id: UUID4) -> Any | None:
        """The abstract buying an item from the shop.

        Args:
            item_id (int): The ID of the item to be bought.
            player_id (UUID4): The ID of the player buying the item.

        Returns:
            Any | None: The purchased item data if successful.
        """