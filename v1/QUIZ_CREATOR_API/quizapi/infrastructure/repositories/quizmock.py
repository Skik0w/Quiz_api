from typing import Iterable
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.core.repositories.iquiz import IQuizRepository
from quizapi.infrastructure.repositories.db import quizzes

class QuizMockRepository(IQuizRepository):

    async def get_quiz_by_id(self, quiz_id: int) -> Quiz | None:
        return next(
            (obj for obj in quizzes if obj.id == quiz_id), None
        )

    async def get_all_quizzes(self) -> Iterable[Quiz]:
        return quizzes

    async def add_quiz(self, data: QuizIn) -> None:
        quizzes.append(data)

    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn
    ) -> Quiz | None:
        if quiz_pos := \
                next(filter(lambda q: q.id == quiz_id, quizzes)):
            quizzes[quiz_pos] = data
            return Quiz(id=0, **data.model_dump())
        return None

    async def delete_quiz(self, quiz_id: int) -> bool:
        if player_pos := \
                next(filter(lambda p: p.id == quiz_id, quizzes)):
            quizzes.remove(player_pos)
            return True