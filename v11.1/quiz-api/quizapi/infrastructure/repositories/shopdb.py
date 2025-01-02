from typing import Any, Iterable

from asyncpg import Record # type: ignore
from sqlalchemy import select, join
from pydantic import UUID4

from quizapi.core.domain.reward import Reward
from quizapi.core.repositories.ishop import IShopRepository
from quizapi.core.domain.shop import Shop, ShopIn
from quizapi.core.domain.shop import Shop
from quizapi.db import (
    reward_table,
    history_table,
    quiz_table,
    player_table,
    shop_table,
    database,
)
from quizapi.infrastructure.dto.rewarddto import RewardDTO
from quizapi.infrastructure.dto.shopdto import ShopDTO
from quizapi.infrastructure.dto.shopdto import ShopDTO
from sqlalchemy import and_

class ShopRepository(IShopRepository):

    async def get_all_items(self) -> Iterable[Any]:
        query = (
            select(
                shop_table.c.id,
                shop_table.c.name,
                shop_table.c.value,
                shop_table.c.quiz_id,
            )
            .order_by(
                shop_table.c.id.asc()
            )
        )

        shops = await database.fetch_all(query)
        return [ShopDTO.from_record(shop) for shop in shops]

    async def sell_item(self, reward_id, player_id: UUID4) -> Any | None:
        reward_query = (
            select(reward_table)
            .where(
                (reward_table.c.id == reward_id) & (reward_table.c.player_id == player_id)
            )
        )
        reward = await database.fetch_one(reward_query)
        if not reward:
            return None

        reward_value = reward["value"]
        reward_quiz = reward["quiz_id"]
        reward_name = reward["reward"]

        update_balance_query = (
            player_table.update()
            .where(player_table.c.id == player_id)
            .values(balance=player_table.c.balance + reward_value)
        )
        await database.execute(update_balance_query)

        delete_reward_query = (
            reward_table.delete()
            .where(reward_table.c.id == reward_id)
        )
        await database.execute(delete_reward_query)

        insert_shop_query = (
            shop_table.insert()
            .values(
                name=reward_name,
                value=reward_value,
                quiz_id=reward_quiz,
            )
        )
        new_shop_id = await database.execute(insert_shop_query)
        new_shop = await self._get_by_id(new_shop_id)
        return Shop(**dict(new_shop)) if new_shop else None

    async def buy_item(self, shop_item_id: int, player_id: UUID4) -> Any | None:

        shop_item_query = (
            shop_table.select()
            .where(
                shop_table.c.id == shop_item_id
            )
        )
        shop_item = await database.fetch_one(shop_item_query)

        if not shop_item:
            return None

        item_name = shop_item["name"]
        item_value = shop_item["value"]
        item_quiz_id = shop_item["quiz_id"]

        player_query = player_table.select().where(player_table.c.id == player_id)
        player = await database.fetch_one(player_query)

        if not player or player["balance"] < item_value:
            return None

        update_balance_query = (
            player_table.update()
            .where(player_table.c.id == player_id)
            .values(balance=player_table.c.balance - item_value)
        )
        await database.execute(update_balance_query)

        delete_shop_item_query = (
            shop_table.delete()
            .where(
                shop_table.c.id == shop_item_id
            )
        )
        await database.execute(delete_shop_item_query)

        insert_reward_query = reward_table.insert().values(
            player_id=player_id,
            quiz_id=item_quiz_id,
            reward=item_name,
            value=item_value,
        )

        new_reward_id = await database.execute(insert_reward_query)
        new_reward = await self._get_reward_by_id(new_reward_id)
        return Reward(**dict(new_reward)) if new_reward else None


    async def _get_by_id(self, shop_id: int) -> Record | None:
        query = (
            shop_table.select()
            .where(shop_table.c.id == shop_id)
            .order_by(shop_table.c.id.asc())
        )
        return await database.fetch_one(query)

    async def _get_reward_by_id(self, reward_id: int) -> Record | None:
        query = (
            reward_table.select()
            .where(reward_table.c.id == reward_id)
            .order_by(reward_table.c.id.asc())
        )
        return await database.fetch_one(query)

