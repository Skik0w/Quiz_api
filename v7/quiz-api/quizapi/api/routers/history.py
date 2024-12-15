from typing import Iterable
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from quizapi.container import Container
from quizapi.core.domain.history import History, HistoryIn
from quizapi.infrastructure.dto.historydto import HistoryDTO
from quizapi.infrastructure.services.ihistory import IHistoryService

router = APIRouter()

@router.post("/create", tags=["History"], response_model=History, status_code=201)
@inject
async def create_history(
    history: HistoryIn,
    service: IHistoryService = Depends(Provide[Container.history_service]),
) -> dict:
    new_history = await service.add_history(history)
    return new_history.model_dump() if new_history else {}

@router.get("/all", tags=["History"], response_model=Iterable[HistoryDTO], status_code=200)
@inject
async def get_all_histories(
        service: IHistoryService = Depends(Provide[Container.history_service]),
) -> Iterable:

    histories = await service.get_all_histories()
    return histories

@router.get("/{history_id}", tags=["History"], response_model=HistoryDTO, status_code=200)
@inject
async def get_history_by_id(
        history_id: int,
        service: IHistoryService = Depends(Provide[Container.history_service]),
) -> dict:

    if history := await service.get_history_by_id(history_id):
        return history.model_dump()
    raise HTTPException(status_code=404, detail="History not found")

@router.get("/player/{player_id}", tags=["History"], response_model=Iterable[History], status_code=200)
@inject
async def get_history_by_player(
        player_id: int,
        service: IHistoryService = Depends(Provide[Container.history_service]),
) -> Iterable:

    histories = await service.get_history_by_player(player_id)
    return histories

@router.put("/{history_id}", tags=["History"], response_model=History, status_code=201)
@inject
async def update_history(
    history_id: int,
    updated_history: HistoryIn,
    service: IHistoryService = Depends(Provide[Container.history_service]),
) -> dict:
    if await service.get_history_by_id(history_id=history_id):
        updated = await service.update_history(
            history_id=history_id,
            data=updated_history,
        )
        if updated:
            return updated.model_dump()
        raise HTTPException(status_code=500, detail="Failed to update history")
    raise HTTPException(status_code=404, detail="History not found")


@router.delete("/{history_id}", tags=["History"], status_code=204)
@inject
async def delete_history(
    history_id: int,
    service: IHistoryService = Depends(Provide[Container.history_service]),
) -> None:

    if await service.get_history_by_id(history_id=history_id):
        await service.delete_history(history_id)
        return

    raise HTTPException(status_code=404, detail="History not found")