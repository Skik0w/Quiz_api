from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from quizapi.container import Container
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.infrastructure.services.iquiz import IQuizService

router = APIRouter()

@router.post("/create", response_model=Quiz, status_code=201)
@inject
async def create_quiz(
    quiz: QuizIn,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> dict:

    await service.add_quiz(quiz)
    return {**quiz.model_dump(),"id":0}

@router.get("/all", response_model=list[Quiz], status_code=200)
@inject
async def get_all_quizzes(
        service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> List:

    quizzes = await service.get_all_quizzes()
    return [{**quiz.model_dump(), "id": 0}
            for i, quiz in enumerate(quizzes)]

@router.get("/{quiz_id}", response_model=Quiz, status_code=200)
@inject
async def get_quiz_by_id(
        quiz_id: int,
        service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> dict | None:

    if quiz := await service.get_quiz_by_id(quiz_id=quiz_id):
        return {**quiz.model_dump(), "id": quiz.id}
    raise HTTPException(status_code=404, detail="Quiz not found")

@router.put("/{quiz_id}", response_model=Quiz, status_code=201)
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


@router.delete("/{quiz_id}", status_code=204)
@inject
async def delete_quiz(
    quiz_id: int,
    service: IQuizService = Depends(Provide[Container.quiz_service]),
) -> None:

    if await service.get_quiz_by_id(quiz_id=quiz_id):
        await service.delete_quiz(quiz_id)

        return

    raise HTTPException(status_code=404, detail="Quiz not found")