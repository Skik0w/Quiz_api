from typing import Iterable
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from quizapi.container import Container
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.infrastructure.dto.quizdto import QuizDTO
from quizapi.infrastructure.services.iquiz import IQuizService

router = APIRouter()

@router.post("/create", tags=["Quiz"], response_model=Quiz, status_code=201)
@inject
async def create_quiz(
    quiz: QuizIn,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> dict:
    new_quiz = await service.add_quiz(quiz)
    return new_quiz.model_dump() if new_quiz else {}

@router.get("/all", tags=["Quiz"], response_model=Iterable[QuizDTO], status_code=200)
@inject
async def get_all_quizzes(
        service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> Iterable:

    quizzes = await service.get_all_quizzes()
    return quizzes

@router.get("/{quiz_id}", tags=["Quiz"], response_model=QuizDTO, status_code=200)
@inject
async def get_quiz_by_id(
        quiz_id: int,
        service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> dict:

    if quiz := await service.get_quiz_by_id(quiz_id):
        return quiz.model_dump()
    raise HTTPException(status_code=404, detail="Quiz not found")

@router.put("/{quiz_id}", tags=["Quiz"], response_model=Quiz, status_code=201)
@inject
async def update_quiz(
    quiz_id: int,
    updated_quiz: QuizIn,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> dict:

    if await service.get_quiz_by_id(quiz_id=quiz_id):
        await service.update_quiz(
            quiz_id=quiz_id,
            data=updated_quiz,
        )
        return {**updated_quiz.model_dump(), "id": quiz_id}
    raise HTTPException(status_code=404, detail="Quiz not found")


@router.delete("/{quiz_id}", tags=["Quiz"], status_code=204)
@inject
async def delete_quiz(
    quiz_id: int,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> None:

    if await service.get_quiz_by_id(quiz_id=quiz_id):
        await service.delete_quiz(quiz_id)
        return

    raise HTTPException(status_code=404, detail="Quiz not found")

@router.get("/share/{quiz_id}", tags=["Quiz"], status_code=200)
@inject
async def share_quiz(
    quiz_id: int,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> dict:
    if await service.get_quiz_by_id(quiz_id=quiz_id):
        shared_quiz = await service.share_quiz(quiz_id)
        return shared_quiz.model_dump()
    raise HTTPException(status_code=404, detail="Quiz not found")