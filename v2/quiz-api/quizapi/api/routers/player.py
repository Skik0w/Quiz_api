from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from quizapi.container import Container
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.infrastructure.services.iplayer import IPlayerService

router = APIRouter()

@router.post("/create", response_model=Player, status_code=201)
@inject
async def create_player(
        player: PlayerIn,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> dict:

    await service.add_player(player)
    return {**player.model_dump(), "id": 0}

@router.get("/all", response_model=list[Player], status_code=200)
@inject
async def get_all_players(
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> list:

    players = await service.get_all_players()
    return [{**player.model_dump(), "id":0}
            for i, player in enumerate(players)]

@router.get("/{player_id}", response_model=Player, status_code=200)
@inject
async def get_player_by_id(
        player_id: int,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> dict:
    if player := await service.get_player_by_id(player_id=player_id):
        return {**player.model_dump(), "id": player_id}
    raise HTTPException(status_code=404, detail="Player not found")

@router.put("/{player_id}", response_model=Player, status_code=201)
@inject
async def update_player(
        player_id: int,
        updated_player: PlayerIn,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> dict:

    if await service.get_player_by_id(player_id=player_id):
        await service.update_player(
            player_id=player_id,
            data=updated_player,
        )
        return {**updated_player.model_dump(), "id": player_id}
    raise HTTPException(status_code=404, detail="Player not found")

@router.delete("/{player_id}", status_code=204)
@inject
async def delete_player(
        player_id: int,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> None:

    if await service.get_player_by_id(player_id=player_id):
        await service.delete_player(player_id)

        return

    raise HTTPException(status_code=404, detail="Player not found")