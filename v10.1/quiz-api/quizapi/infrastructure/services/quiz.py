from typing import Iterable
from quizapi.core.domain.quiz import Quiz, QuizIn
from quizapi.core.repositories.iquiz import IQuizRepository
from quizapi.infrastructure.dto.quizdto import QuizDTO
from quizapi.infrastructure.services.iquiz import IQuizService

class QuizService(IQuizService):

    _repository: IQuizRepository

    def __init__(self, repository: IQuizRepository):

        self._repository = repository

    async def get_all_quizzes(self) -> Iterable[QuizDTO]:
        return await self._repository.get_all_quizzes()

    async def get_quiz_by_id(self, quiz_id: int) -> QuizDTO | None:
        return await self._repository.get_quiz_by_id(quiz_id)

    async def add_quiz(self, data: QuizIn) -> Quiz | None:
        return await self._repository.add_quiz(data)

    async def update_quiz(
            self,
            quiz_id: int,
            data: QuizIn
    ) -> Quiz | None:
        return await self._repository.update_quiz(
            quiz_id=quiz_id,
            data=data,
        )

    async def delete_quiz(self, quiz_id: int) -> bool:
        return await self._repository.delete_quiz(quiz_id)

    async def share_quiz(self, quiz_id: int) -> Quiz | None:
        quiz = await self.get_quiz_by_id(quiz_id)
        return await self._repository.update_quiz(
            quiz_id=quiz_id,
            data=QuizIn(
                title=quiz.title,
                description=quiz.description,
                shared=True,
                reward=quiz.reward,
            )
        )