from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

class QuizDTO(BaseModel):
    id: int
    questions: list[QuizDTO]
    player_id: int
    description: Optional[str] = None
