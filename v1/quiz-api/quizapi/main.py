from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from quizapi.container import Container
from quizapi.api.routers.quiz import router as quiz_router


container = Container()
container.wire(modules=[
    "quizapi.api.routers.quiz",
])

app = FastAPI()
app.include_router(quiz_router, prefix="/quiz")

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:

    return await http_exception_handler(request, exception)
