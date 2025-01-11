"""A module containing player-related routers."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from quizapi.infrastructure.utils import consts

from quizapi.container import Container
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.infrastructure.dto.tokendto import TokenDTO
from quizapi.infrastructure.dto.playerdto import PlayerDTO
from quizapi.infrastructure.services.iplayer import IPlayerService

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.post("/register", tags=["Player"], response_model=PlayerDTO, status_code=201)
@inject
async def register_player(
    player: PlayerIn,
    service: IPlayerService = Depends(Provide[Container.player_service]),
) -> dict:
    """A router coroutine for registering new player

    Args:
        player (PlayerIn): The player input data.
        service (IPlayerService, optional): The injected player service.

    Raises:
        HTTPException: 400 if player already exist.

    Returns:
        dict: The player DTO details.
    """
    if new_player := await service.register_player(player):
        return PlayerDTO(**dict(new_player)).model_dump()

    raise HTTPException(status_code=400, detail="The player with provided email already exists")

@router.post("/token", tags=["Player"], response_model=TokenDTO, status_code=200)
@inject
async def authenticate_player(
        player: PlayerIn,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> dict:
    """A router coroutine for authenticating players.

    Args:
        player (PlayerIn): The player input data.
        service (IPlayerService, optional): The injected player service.

    Raises:
        HTTPException: 401 if provided incorrect credentials.

    Returns:
        dict: The token DTO details.
    """
    if token_details := await service.authenticate_player(player):
        print("Player confirmed")
        return token_details.model_dump()

    raise HTTPException(status_code=401, detail="Provided incorrect credentials")

@router.get("/balance", tags=["Player"], response_model=int)
@inject
async def show_balance(
        service: IPlayerService = Depends(Provide[Container.player_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> int:
    """An endpoint for getting the player's balance.

    Args:
        service (IPlayerService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        int: The player's balance.
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    player_uuid = token_payload.get("sub")

    balance = await service.show_balance(player_uuid)
    return balance
