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
        quiz_pos = next(
            (index for index, quiz in enumerate(quizzes) if quiz.id == quiz_id),None
        )
        if quiz_pos is None:
            return None
        updated_quiz = Quiz(id=quiz_id, **data.model_dump())
        quizzes[quiz_pos] = updated_quiz
        return quizzes[quiz_pos]

    async def delete_quiz(self, quiz_id: int) -> bool:
        if quiz_pos := \
                next(filter(lambda x: x.id == quiz_id, quizzes)):
            quizzes.remove(quiz_pos)
            return True