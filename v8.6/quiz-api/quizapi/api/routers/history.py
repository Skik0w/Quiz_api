from typing import Iterable
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from pydantic import UUID4

from quizapi.infrastructure.utils import consts
from quizapi.container import Container
from quizapi.core.domain.history import History, HistoryIn, HistoryBroker
from quizapi.infrastructure.dto.historydto import HistoryDTO
from quizapi.infrastructure.services.ihistory import IHistoryService

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.post("/create", tags=["History"], response_model=History, status_code=201)
@inject
async def create_history(
    history: HistoryIn,
    service: IHistoryService = Depends(Provide[Container.history_service]),
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

    extended_history_data = HistoryBroker(
        player_id=player_uuid,
        **history.model_dump()
    )
    new_history = await service.add_history(extended_history_data)
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
        player_id: UUID4,
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

    if history_data := await service.get_history_by_id(history_id=history_id):
        if str(history_data.player_id) != player_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_history_data = HistoryBroker(
            player_id=player_uuid,
            **updated_history.model_dump()
        )
        updated_history_data = await service.update_history(
            history_id=history_id,
            data=extended_history_data,
        )
        return updated_history_data.model_dump() if updated_history_data else {}
    raise HTTPException(status_code=404, detail="History not found")


@router.delete("/{history_id}", tags=["History"], status_code=204)
@inject
async def delete_history(
    history_id: int,
    service: IHistoryService = Depends(Provide[Container.history_service]),
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

    if history_data := await service.get_history_by_id(history_id=history_id):
        if str(history_data.player_id) != player_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")
        await service.delete_history(history_id)
        return
    raise HTTPException(status_code=404, detail="History not found")