from typing import Iterable
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from quizapi.core.domain.reward import Reward
from quizapi.infrastructure.utils import consts
from quizapi.container import Container
from quizapi.core.domain.shop import Shop, ShopIn
from quizapi.infrastructure.dto.shopdto import ShopDTO
from quizapi.infrastructure.services.ishop import IShopService

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.get("/all", tags=["Shop"], response_model=Iterable[ShopDTO], status_code=200)
@inject
async def get_all_items(
        service: IShopService = Depends(Provide[Container.shop_service]),
) -> Iterable:

    shops = await service.get_all_items()
    return shops

@router.post("/sell/{reward_id}", tags=["Shop"], response_model=Shop, status_code=200)
@inject
async def sell_item(
    reward_id: int,
    service: IShopService = Depends(Provide[Container.shop_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    player_uuid = token_payload.get("sub")

    if not player_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    new_shop = await service.sell_item(reward_id, player_uuid)

    if not new_shop:
        raise HTTPException(status_code=400, detail="Item does not exist or does not belong to the user.")

    return new_shop.model_dump() if new_shop else {}

@router.post("/buy/{reward_id}", tags=["Shop"], response_model=Reward, status_code=200)
@inject
async def buy_item(
    reward_id: int,
    service: IShopService = Depends(Provide[Container.shop_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    player_uuid = token_payload.get("sub")

    if not player_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    new_reward = await service.buy_item(reward_id, player_uuid)

    if not new_reward:
        raise HTTPException(status_code=400, detail="Item does not exist, insufficient funds, or other error.")

    return new_reward.model_dump() if new_reward else {}