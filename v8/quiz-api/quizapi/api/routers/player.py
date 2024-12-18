from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from quizapi.container import Container
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.infrastructure.dto.tokendto import TokenDTO
from quizapi.infrastructure.dto.playerdto import PlayerDTO
from quizapi.infrastructure.services.iplayer import IPlayerService

router = APIRouter()

@router.post("/register", tags=["Player"], response_model=PlayerDTO, status_code=201)
@inject
async def register_player(
    player: PlayerIn,
    service: IPlayerService = Depends(Provide[Container.player_service]),
) -> dict:

    if new_player := await service.register_player(player):
        return PlayerDTO(**dict(new_player)).model_dump()

    raise HTTPException(status_code=400, detail="The player with provided email already exists")

@router.post("/token", tags=["Player"], response_model=TokenDTO, status_code=200)
@inject
async def authenticate_player(
        player: PlayerIn,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> dict:

    if token_details := await service.authenticate_player(player):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(status_code=400, detail="Provided incorrect credentials")