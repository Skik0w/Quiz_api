"""A module containing question endpoints."""

from typing import Iterable
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from quizapi.infrastructure.utils import consts
from quizapi.container import Container
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.infrastructure.dto.questiondto import QuestionDTO
from quizapi.infrastructure.services.iquestion import IQuestionService
from quizapi.infrastructure.services.iquiz import IQuizService

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.post("/create", tags=["Question"], response_model=Question, status_code=201)
@inject
async def create_question(
    question: QuestionIn,
    service: IQuestionService = Depends(Provide[Container.question_service]),
    quiz_service: IQuizService = Depends(Provide[Container.quiz_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating a new question.

    Args:
        question (QuestionIn): The question data.
        service (IQuestionService, optional): The injected service dependency.
        quiz_service (IQuizService, optional): The injected quiz service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.
        HTTPException: 404 if quiz is not found.

    Returns:
        dict: The new created question attributes.
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

    quiz = await quiz_service.get_quiz_by_id(question.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if str(quiz.player_id) != player_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    new_question = await service.add_question(question)
    return new_question.model_dump() if new_question else {}

@router.get("/all", tags=["Question"], response_model=Iterable[QuestionDTO], status_code=200)
@inject
async def get_all_questions(
        service: IQuestionService = Depends(Provide[Container.question_service]),
) -> Iterable:
    """An endpoint for getting all questions.

    Args:
        service (IQuestionService, optional): The injected service dependency.

    Returns:
        Iterable: The question attributes collection.
    """
    questions = await service.get_all_questions()
    return questions

@router.get("/{question_id}", tags=["Question"], response_model=QuestionDTO, status_code=200)
@inject
async def get_question_by_id(
        question_id: int,
        service: IQuestionService = Depends(Provide[Container.question_service]),
) -> dict:
    """An endpoint for getting a question by ID.

    Args:
        question_id (int): The question ID.
        service (IQuestionService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if question is not found.

    Returns:
        dict: The question details.
    """
    if question := await service.get_question_by_id(question_id):
        return question.model_dump()
    raise HTTPException(status_code=404, detail="Question not found")

@router.get("/quiz/{quiz_id}", tags=["Question"], response_model=Iterable[Question], status_code=200)
@inject
async def get_questions_by_quiz(
        quiz_id: int,
        service: IQuestionService = Depends(Provide[Container.question_service]),
) -> Iterable:
    """An endpoint for getting questions by quiz ID.

    Args:
        quiz_id (int): The quiz ID.
        service (IQuestionService, optional): The injected service dependency.

    Returns:
        Iterable: A collection of questions for the given quiz.
    """
    questions = await service.get_questions_by_quiz(quiz_id)
    return questions

@router.put("/{question_id}", tags=["Question"], response_model=Question, status_code=201)
@inject
async def update_question(
    question_id: int,
    updated_question: QuestionIn,
    service: IQuestionService = Depends(Provide[Container.question_service]),
    quiz_service: IQuizService = Depends(Provide[Container.quiz_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    """An endpoint for updating a question.

    Args:
        question_id (int): The question ID.
        updated_question (QuestionIn): The updated question details.
        service (IQuestionService, optional): The injected service dependency.
        quiz_service (IQuizService, optional): The injected quiz service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.
        HTTPException: 404 if question is not found.

    Returns:
        dict: The updated question details.
    """
    player_uuid = token_payload.get("sub")

    if not player_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if question_data := await service.get_question_by_id(question_id=question_id):
        if updated_question.quiz_id != question_data.quiz.id:
            raise HTTPException(status_code=403, detail="Cannot change quiz ownership of the question")

        if quiz_data := await quiz_service.get_quiz_by_id(quiz_id=question_data.quiz.id):
            if str(quiz_data.player_id) != player_uuid:
                raise HTTPException(status_code=403, detail="Unauthorized")

            updated_question_data = await service.update_question(
                question_id=question_id,
                data=updated_question,
            )
            return updated_question_data.model_dump() if updated_question_data else {}

    raise HTTPException(status_code=404, detail="Question not found")

@router.delete("/{question_id}", tags=["Question"], status_code=204)
@inject
async def delete_question(
    question_id: int,
    service: IQuestionService = Depends(Provide[Container.question_service]),
    quiz_service: IQuizService = Depends(Provide[Container.quiz_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting a question.

    Args:
        question_id (int): The question ID.
        service (IQuestionService, optional): The injected service dependency.
        quiz_service (IQuizService, optional): The injected quiz service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.
        HTTPException: 404 if question is not found.
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

    if question_data := await service.get_question_by_id(question_id=question_id):
        if quiz_data := await quiz_service.get_quiz_by_id(quiz_id=question_data.quiz.id):
            if str(quiz_data.player_id) != player_uuid:
                raise HTTPException(status_code=403, detail="Unauthorized")

            await service.delete_question(question_id)
            return
    raise HTTPException(status_code=404, detail="Question not found")