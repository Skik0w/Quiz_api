from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4
from quizapi.core.domain.reward import RewardIn
from quizapi.core.domain.shop import ShopIn

class IShopRepository(ABC):

    @abstractmethod
    async def get_all_items(self) -> Iterable[Any]:
        """ """

    @abstractmethod
    async def sell_item(self, reward_id: int, player_id: UUID4) -> Any | None:
        """ """

    @abstractmethod
    async def buy_item(self, item_id: int, player_id: UUID4) -> Any | None:
        """ """