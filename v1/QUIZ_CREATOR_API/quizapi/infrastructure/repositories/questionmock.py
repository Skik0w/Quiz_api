from typing import Iterable
from quizapi.core.domain.question import Question, QuestionIn
from quizapi.core.repositories.iquestion import IQuestionRepository
from quizapi.infrastructure.repositories.db import questions

class QuestionMockRepository(IQuestionRepository):

    async def get_question_by_id(self, question_id: int) -> Question | None:
        return next(
            (obj for obj in questions if obj.id == question_id), None
        )

    async def get_all_questions(self) -> Iterable[Question]:
        return questions

    async def add_question(self, question: QuestionIn) -> None:
        questions.append(question)

    async def update_question(
        self,
        question_id: int,
        question: QuestionIn,
    ) -> Question | None:
        if quiz_pos := \
                next(filter(lambda q: q.id == question_id, questions)):
            questions[quiz_pos] = question
            return Question(id=0, **question.model_dump())
        return None

    async def delete_question(self, question_id: int) -> bool:
        if player_pos := \
                next(filter(lambda p: p.id == question_id, questions)):
            questions.remove(player_pos)
            return True