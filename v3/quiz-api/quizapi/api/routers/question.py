from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from quizapi.container import Container
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.infrastructure.services.iquestion import IQuestionService

router = APIRouter()


@router.post("/create", response_model=Question, status_code=201)
@inject
async def create_question(
        question: QuestionIn,
        service: IQuestionService = Depends(Provide[Container.question_service]),
) -> dict:
    await service.add_question(question)
    return {**question.model_dump(), "id": 0}


@router.get("/all", response_model=list[Question], status_code=200)
@inject
async def get_all_questions(
        service: IQuestionService = Depends(Provide[Container.question_service]),
) -> list:
    questions = await service.get_all_questions()
    return [{**question.model_dump(), "id": 0}
            for i, question in enumerate(questions)]


@router.get("/{question_id}", response_model=Question, status_code=200)
@inject
async def get_question_by_id(
        question_id: int,
        service: IQuestionService = Depends(Provide[Container.question_service]),
) -> dict | None:
    if question := await service.get_question_by_id(question_id=question_id):
        return {**question.model_dump(), "id": question.id}
    raise HTTPException(status_code=404, detail="Quiz not found")


@router.put("/{question_id}", response_model=Question, status_code=201)
@inject
async def update_question(
        question_id: int,
        updated_question: QuestionIn,
        service: IQuestionService = Depends(Provide[Container.question_service]),
) -> dict:
    if await service.get_question_by_id(question_id=question_id):
        await service.update_question(
            question_id=question_id,
            data=updated_question,
        )
        return {**updated_question.model_dump(), "id": question_id}
    raise HTTPException(status_code=404, detail="Quiz not found")


@router.delete("/{question_id}", status_code=204)
@inject
async def delete_question(
        question_id: int,
        service: IQuestionService = Depends(Provide[Container.question_service]),
) -> None:
    if await service.get_question_by_id(question_id=question_id):
        await service.delete_question(question_id)

        return

    raise HTTPException(status_code=404, detail="Quiz not found")