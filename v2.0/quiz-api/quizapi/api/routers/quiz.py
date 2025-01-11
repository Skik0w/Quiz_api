"""A module containing quiz endpoints."""

from typing import Iterable
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from quizapi.infrastructure.utils import consts
from quizapi.container import Container
from quizapi.core.domain.quiz import Quiz, QuizIn, QuizBroker
from quizapi.infrastructure.dto.quizdto import QuizDTO
from quizapi.infrastructure.services.iquiz import IQuizService

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.post("/create", tags=["Quiz"], response_model=Quiz, status_code=201)
@inject
async def create_quiz(
    quiz: QuizIn,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating a new quiz.

    Args:
        quiz (QuizIn): The quiz data.
        service (IQuizService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.
        HTTPException: 404 if the reward name is already taken.

    Returns:
        dict: The new created quiz attributes.
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

    extended_quiz_data = QuizBroker(
        player_id=player_uuid,
        **quiz.model_dump(),
    )
    new_quiz = await service.add_quiz(extended_quiz_data)
    if not new_quiz:
        raise HTTPException(status_code=404, detail="Reward name is already taken")
    return new_quiz.model_dump() if new_quiz else {}

@router.get("/all", tags=["Quiz"], response_model=Iterable[QuizDTO], status_code=200)
@inject
async def get_all_quizzes(
        service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> Iterable:
    """An endpoint for getting all quizzes.

    Args:
        service (IQuizService, optional): The injected service dependency.

    Returns:
        Iterable: A collection of all quizzes.
    """
    quizzes = await service.get_all_quizzes()
    return quizzes

@router.get("/{quiz_id}", tags=["Quiz"], response_model=QuizDTO, status_code=200)
@inject
async def get_quiz_by_id(
        quiz_id: int,
        service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> dict:
    """An endpoint for getting a quiz by ID.

    Args:
        quiz_id (int): The quiz ID.
        service (IQuizService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if quiz is not found.

    Returns:
        dict: The quiz details.
    """
    if quiz := await service.get_quiz_by_id(quiz_id):
        return quiz.model_dump()
    raise HTTPException(status_code=404, detail="Quiz not found")

@router.put("/{quiz_id}", tags=["Quiz"], response_model=Quiz, status_code=201)
@inject
async def update_quiz(
    quiz_id: int,
    updated_quiz: QuizIn,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating a quiz.

    Args:
        quiz_id (int): The quiz ID.
        updated_quiz (QuizIn): The updated quiz details.
        service (IQuizService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.
        HTTPException: 404 if quiz is not found or reward name is already taken.

    Returns:
        dict: The updated quiz details.
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

    if quiz_data := await service.get_quiz_by_id(quiz_id=quiz_id):
        if str(quiz_data.player_id) != player_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_quiz_data = QuizBroker(
            player_id=player_uuid,
            **updated_quiz.model_dump(),
        )
        updated_quiz_data = await service.update_quiz(
            quiz_id=quiz_id,
            data=extended_quiz_data,
        )
        if  not updated_quiz_data:
            raise HTTPException(status_code=404, detail="Reward name is already taken")
        return updated_quiz_data.model_dump() if updated_quiz else {}
    raise HTTPException(status_code=404, detail="Quiz not found")

@router.put("/share/{quiz_id}", tags=["Quiz"], status_code=200)
@inject
async def share_quiz(
    quiz_id: int,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for sharing a quiz.

        Args:
            quiz_id (int): The quiz ID.
            service (IQuizService, optional): The injected service dependency.
            credentials (HTTPAuthorizationCredentials, optional): The credentials.

        Raises:
            HTTPException: 403 if unauthorized.
            HTTPException: 404 if quiz is not found.

        Returns:
            dict: The shared quiz details.
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

    if quiz_data := await service.get_quiz_by_id(quiz_id=quiz_id):
        if str(quiz_data.player_id) != player_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")
        shared_quiz = await service.share_quiz(quiz_id)
        return shared_quiz.model_dump()
    raise HTTPException(status_code=404, detail="Quiz not found")


@router.delete("/{quiz_id}", tags=["Quiz"], status_code=204)
@inject
async def delete_quiz(
    quiz_id: int,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting quiz.

    Args:
        quiz_id (int): The quiz ID.
        service (IQuizService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if quiz is not found.
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

    if quiz_data := await service.get_quiz_by_id(quiz_id=quiz_id):
        if str(quiz_data.player_id) != player_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")
        await service.delete_quiz(quiz_id)
        return

    raise HTTPException(status_code=404, detail="Quiz not found")