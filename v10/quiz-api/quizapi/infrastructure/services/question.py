from typing import Iterable
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.core.repositories.iquestion import IQuestionRepository
from quizapi.infrastructure.dto.questiondto import QuestionDTO
from quizapi.infrastructure.services.iquestion import IQuestionService

class QuestionService(IQuestionService):

    _repository: IQuestionRepository

    def __init__(self, repository: IQuestionRepository):
        self._repository = repository

    async def get_all_questions(self) -> Iterable[QuestionDTO]:
        return await self._repository.get_all_questions()

    async def get_question_by_id(self, question_id: int) -> QuestionDTO | None:
        return await self._repository.get_question_by_id(question_id)

    async def get_questions_by_quiz(self, quiz_id: int) -> Iterable[QuestionDTO] | None:
        return await self._repository.get_questions_by_quiz(quiz_id)

    async def add_question(self, data: QuestionIn) -> None:
        return await self._repository.add_question(data)

    async def update_question(
        self,
        question_id: int,
        data: QuestionIn,
    ) -> Question | None:
        return await self._repository.update_question(
            question_id=question_id,
            data=data,
        )

    async def delete_question(self, question_id: int) -> bool:
        return await self._repository.delete_question(question_id)