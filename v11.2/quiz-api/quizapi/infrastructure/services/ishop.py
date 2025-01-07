from abc import ABC, abstractmethod
from typing import Iterable

from pydantic.v1 import UUID4

from quizapi.core.domain.reward import RewardIn, Reward
from quizapi.core.domain.shop import Shop, ShopIn
from quizapi.infrastructure.dto.shopdto import ShopDTO


class IShopService(ABC):

    @abstractmethod
    async def get_all_items(self) -> Iterable[ShopDTO]:
        """ """

    @abstractmethod
    async def sell_item(self, reward_id: int, player_id: UUID4) -> Shop | None:
        """ """

    @abstractmethod
    async def buy_item(self, item_id: int, player_id: UUID4) -> Reward:
        """ """