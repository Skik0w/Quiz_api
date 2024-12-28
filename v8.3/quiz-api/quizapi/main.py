from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from quizapi.container import Container
from quizapi.api.routers.player import router as player_router
from quizapi.api.routers.question import router as question_router
from quizapi.api.routers.quiz import router as quiz_router
from quizapi.api.routers.history import router as history_router
from quizapi.db import database
from quizapi.db import init_db

container = Container()
container.wire(modules=[
    "quizapi.api.routers.quiz",
    "quizapi.api.routers.question",
    "quizapi.api.routers.player",
    "quizapi.api.routers.history",
])

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    await init_db()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="Quiz API",
    description= """
    Aplikacja do tworzenia quizów
    
    Funkcjonalności:
    - Tworzenie i zarządzanie quizami przez użytkowników.
    - Dodawanie historii rozgrywek.
    - Tworzenie i zarządzanie turniejami.
    - System nagród i giełda między użytkownikami.
    """,
    lifespan=lifespan
)

app.include_router(quiz_router, prefix="/quiz")
app.include_router(question_router, prefix="/question")
app.include_router(player_router, prefix="/player")
app.include_router(history_router, prefix="/history")

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    return await http_exception_handler(request, exception)