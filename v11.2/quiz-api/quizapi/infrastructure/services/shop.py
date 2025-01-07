from typing import Iterable

from quizapi.core.domain.reward import Reward
from quizapi.core.domain.shop import Shop, ShopIn
from quizapi.core.repositories.ishop import IShopRepository
from quizapi.infrastructure.dto.shopdto import ShopDTO
from quizapi.infrastructure.services.ishop import IShopService

from pydantic import UUID4

class ShopService(IShopService):

    _repository: IShopRepository

    def __init__(self, repository: IShopRepository):

        self._repository = repository

    async def get_all_items(self) -> Iterable[ShopDTO]:
        return await self._repository.get_all_items()

    async def sell_item(self, reward_id: int, player_id: UUID4) -> Shop | None:
        return await self._repository.sell_item(reward_id, player_id)

    async def buy_item(self, reward_id: int, player_id: UUID4) -> Reward | None:
        return await self._repository.buy_item(reward_id, player_id)
