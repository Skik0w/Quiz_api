"""A module containing reward endpoints."""

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
    """An endpoint for collecting a reward.

        Args:
            reward (RewardIn): The reward data.
            service (IRewardService, optional): The injected service dependency.
            credentials (HTTPAuthorizationCredentials, optional): The credentials.

        Raises:
            HTTPException: 403 if unauthorized.
            HTTPException: 400 if no eligible histories or reward cannot be collected.

        Returns:
            dict: The collected reward details.
    """
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
    """An endpoint for getting all rewards.

    Args:
        service (IRewardService, optional): The injected service dependency.

    Returns:
        Iterable: A collection of all rewards.
    """
    rewards = await service.get_all_rewards()
    return rewards

@router.get("/{reward_id}", tags=["Reward"], response_model=RewardDTO, status_code=200)
@inject
async def get_reward_by_id(
        reward_id: int,
        service: IRewardService = Depends(Provide[Container.reward_service]),
) -> dict:
    """An endpoint for getting a reward by ID.

    Args:
        reward_id (int): The reward ID.
        service (IRewardService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if reward is not found.

    Returns:
        dict: The reward details.
    """
    if reward := await service.get_reward_by_id(reward_id):
        return reward.model_dump()
    raise HTTPException(status_code=404, detail="Reward not found")

@router.get("/player/{player_id}", tags=["Reward"], response_model=Iterable[Reward], status_code=200)
@inject
async def get_reward_by_player(
        player_id: UUID4,
        service: IRewardService = Depends(Provide[Container.reward_service]),
) -> Iterable:
    """An endpoint for getting rewards by player ID.

       Args:
           player_id (UUID4): The player's unique ID.
           service (IRewardService, optional): The injected service dependency.

       Returns:
           Iterable: A collection of rewards for the given player.
    """
    rewards = await service.get_rewards_by_player(player_id)
    return rewards

@router.delete("/{reward_id}", tags=["Reward"], status_code=204)
@inject
async def delete_reward(
    reward_id: int,
    service: IRewardService = Depends(Provide[Container.reward_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting reward.

    Args:
        reward_id (int): The reward ID.
        service (IRewardService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if reward is not found.
        HTTPException: 403 if unauthorized.

    Returns:
        dict: Empty if operation finished.
    """
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