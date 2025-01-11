"""Module containing shop service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic.v1 import UUID4

from quizapi.core.domain.reward import Reward
from quizapi.core.domain.shop import Shop, ShopIn
from quizapi.infrastructure.dto.shopdto import ShopDTO


class IShopService(ABC):
    """An abstract class representing protocol of shop service."""

    @abstractmethod
    async def get_all_items(self) -> Iterable[ShopDTO]:
        """The abstract getting all items available in the shop.

        Returns:
            Iterable[ShopDTO]: The collection of all items in the shop.
        """

    @abstractmethod
    async def sell_item(self, reward_id: int, player_id: UUID4) -> Shop | None:
        """The abstract selling an item by a player.

        Args:
            reward_id (int): The ID of the reward item to sell.
            player_id (UUID4): The UUID of the player selling the item.

        Returns:
            Shop | None: The newly added shop item if the sale is successful.
        """

    @abstractmethod
    async def buy_item(self, item_id: int, player_id: UUID4) -> Reward:
        """The abstract purchasing an item from the shop.

        Args:
            item_id (int): The ID of the shop item to buy.
            player_id (UUID4): The UUID of the player buying the item.

        Returns:
            Reward: The purchased reward item.
        """