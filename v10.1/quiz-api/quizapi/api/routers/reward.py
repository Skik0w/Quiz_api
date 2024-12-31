from typing import Iterable
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from quizapi.infrastructure.utils import consts
from quizapi.container import Container
from quizapi.core.domain.reward import Reward, RewardIn, RewardBroker
from quizapi.infrastructure.dto.rewarddto import RewardDTO
from quizapi.infrastructure.services.ireward import IRewardService

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.post("/collect", tags=["Reward"], response_model=Reward, status_code=201)
@inject
async def collect_reward(
    reward: RewardIn,
    service: IRewardService = Depends(Provide[Container.reward_service]),
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

    extended_reward_data = RewardBroker(
        player_id=player_uuid,
        **reward.model_dump(),
    )
    new_reward = await service.collect_reward(extended_reward_data)
    if not new_reward:
        raise HTTPException(status_code=400, detail="No eligible histories or reward could not be collected.")
    return new_reward.model_dump()

@router.get("/all", tags=["Reward"], response_model=Iterable[RewardDTO], status_code=200)
@inject
async def get_all_rewards(
        service: IRewardService = Depends(Provide[Container.reward_service]),
) -> Iterable:

    rewards = await service.get_all_rewards()
    return rewards

@router.get("/{reward_id}", tags=["Reward"], response_model=RewardDTO, status_code=200)
@inject
async def get_reward_by_id(
        reward_id: int,
        service: IRewardService = Depends(Provide[Container.reward_service]),
) -> dict:

    if reward := await service.get_reward_by_id(reward_id):
        return reward.model_dump()
    raise HTTPException(status_code=404, detail="Reward not found")

@router.get("/player/{player_id}", tags=["Reward"], response_model=Iterable[Reward], status_code=200)
@inject
async def get_reward_by_player(
        player_id: UUID4,
        service: IRewardService = Depends(Provide[Container.reward_service]),
) -> Iterable:

    rewards = await service.get_rewards_by_player(player_id)
    return rewards

@router.put("/{reward_id}", tags=["Reward"], response_model=Reward, status_code=201)
@inject
async def update_reward(
    reward_id: int,
    updated_reward: RewardIn,
    service: IRewardService = Depends(Provide[Container.reward_service]),
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

    if reward_data := await service.get_reward_by_id(reward_id=reward_id):
        if str(reward_data.player_id) != player_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_reward_data = RewardBroker(
            player_id=player_uuid,
            **updated_reward.model_dump(),
        )
        updated_reward_data = await service.update_reward(
            reward_id=reward_id,
            data=extended_reward_data,
        )
        return updated_reward_data.model_dump() if updated_reward else {}

    raise HTTPException(status_code=404, detail="Reward not found")

@router.delete("/{reward_id}", tags=["Reward"], status_code=204)
@inject
async def delete_reward(
    reward_id: int,
    service: IRewardService = Depends(Provide[Container.reward_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    player_uuid = token_payload.get("sub")

    if not player_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if reward_data := await service.get_reward_by_id(reward_id=reward_id):
        if str(reward_data.player_id) != player_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")
        await service.delete_reward(reward_id)
        return

    raise HTTPException(status_code=404, detail="Reward not found")



@router.get("/compare", tags=["Reward"], status_code=200)
@inject
async def compare_rewards(
    reward_id_1: int,
    reward_id_2: int,
    service: IRewardService = Depends(Provide[Container.reward_service]),
) -> dict:
    # Pobierz pierwszą nagrodę
    reward_1 = await service.get_reward_by_id(reward_id_1)
    if not reward_1:
        raise HTTPException(status_code=404, detail=f"Reward with id {reward_id_1} not found")

    # Pobierz drugą nagrodę
    reward_2 = await service.get_reward_by_id(reward_id_2)
    if not reward_2:
        raise HTTPException(status_code=404, detail=f"Reward with id {reward_id_2} not found")

    # Porównaj nagrody (np. po nazwie, quiz_id lub player_id)
    are_equal = reward_1.reward == reward_2.reward

    return {
        "reward_1": reward_1.model_dump(),
        "reward_2": reward_2.model_dump(),
        "are_equal": are_equal
    }