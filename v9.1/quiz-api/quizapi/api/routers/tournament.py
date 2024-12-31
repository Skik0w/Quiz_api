from typing import Iterable
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from quizapi.infrastructure.utils import consts
from quizapi.container import Container
from quizapi.core.domain.tournament import Tournament, TournamentIn
from quizapi.infrastructure.dto.tournamentdto import TournamentDTO
from quizapi.infrastructure.services.itournament import ITournamentService

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.post("/create", tags=["Tournament"], response_model=Tournament, status_code=201)
@inject
async def create_tournament(
    tournament: TournamentIn,
    service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> dict:
    new_tournament = await service.add_tournament(tournament)
    return new_tournament.model_dump() if new_tournament else None

@router.get("/all", tags=["Tournament"], response_model=Iterable[TournamentDTO], status_code=200)
@inject
async def get_all_tournaments(
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> Iterable:

    tournaments = await service.get_all_tournaments()
    return tournaments

@router.get("/{tournament_id}", tags=["Tournament"], response_model=TournamentDTO, status_code=200)
@inject
async def get_tournament_by_id(
        tournament_id: int,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> dict:

    if tournament := await service.get_tournament_by_id(tournament_id):
        return tournament.model_dump()
    raise HTTPException(status_code=404, detail="Tournament not found")

@router.put("/{tournament_id}", tags=["Tournament"], response_model=Tournament, status_code=201)
@inject
async def update_tournament(
        tournament_id: int,
        updated_tournament: TournamentIn,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> dict:
    if await service.get_tournament_by_id(tournament_id=tournament_id):
        updated = await service.update_tournament(
            tournament_id=tournament_id,
            data=updated_tournament,
            #participants=updated_tournament.participants,
        )
        if updated:
            return updated.model_dump()
        raise HTTPException(status_code=500, detail="Failed to update tournament")
    raise HTTPException(status_code=404, detail="Tournament not found")

@router.delete("/{tournament_id}", tags=["Tournament"], status_code=204)
@inject
async def delete_tournament(
        tournament_id: int,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> None:

    if await service.get_tournament_by_id(tournament_id=tournament_id):
        await service.delete_tournament(tournament_id)
        return

    raise HTTPException(status_code=404, detail="Tournament not found")

@router.post("/{tournament_id}/join", tags=["Tournament"], response_model=Tournament, status_code=200)
@inject
async def join_tournament(
        tournament_id: int,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
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

    updated_tournament = await service.join_tournament(tournament_id, UUID4(player_uuid))
    if not updated_tournament:
        raise HTTPException(status_code=400, detail="Failed to join tournament or already a participant.")

    return updated_tournament.model_dump()


@router.post("/{tournament_id}/leave", tags=["Tournament"], response_model=Tournament, status_code=200)
@inject
async def leave_tournament(
        tournament_id: int,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
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

    updated_tournament = await service.leave_tournament(tournament_id, UUID4(player_uuid))
    if not updated_tournament:
        raise HTTPException(status_code=400, detail="Failed to leave tournament or not a participant.")

    return updated_tournament.model_dump()