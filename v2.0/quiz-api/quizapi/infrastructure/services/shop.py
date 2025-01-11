"""Module containing shop service implementation."""

from typing import Iterable

from quizapi.core.domain.reward import Reward
from quizapi.core.domain.shop import Shop, ShopIn
from quizapi.core.repositories.ishop import IShopRepository
from quizapi.infrastructure.dto.shopdto import ShopDTO
from quizapi.infrastructure.services.ishop import IShopService

from pydantic import UUID4

class ShopService(IShopService):
    """A class implementing the shop service."""

    _repository: IShopRepository

    def __init__(self, repository: IShopRepository):
        """The initializer of the `shop service`.

        Args:
            repository (IShopRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_all_items(self) -> Iterable[ShopDTO]:
        """Getting all shop items from the repository.

        Returns:
            Iterable[ShopDTO]: A collection of all shop items.
        """
        return await self._repository.get_all_items()

    async def sell_item(self, reward_id: int, player_id: UUID4) -> Shop | None:
        """Selling an item and adding it to the shop.

        Args:
            reward_id (int): The ID of the reward to sell.
            player_id (UUID4): The UUID of the player selling the item.

        Returns:
            Shop | None: The shop entry of the sold item if successful, otherwise None.
        """
        return await self._repository.sell_item(reward_id, player_id)

    async def buy_item(self, reward_id: int, player_id: UUID4) -> Reward | None:
        """Buying an item from the shop.

        Args:
            reward_id (int): The ID of the reward to buy.
            player_id (UUID4): The UUID of the player buying the item.

        Returns:
            Reward | None: The newly acquired reward if successful, otherwise None.
        """
        return await self._repository.buy_item(reward_id, player_id)
