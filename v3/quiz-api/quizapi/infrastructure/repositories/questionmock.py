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
        data: QuestionIn,
    ) -> Question | None:
        question_pos = next(
            (index for index, question in enumerate(questions) if question.id == question_id),None
        )
        if question_pos is None:
            return None
        updated_question = Question(id=question_id, **data.model_dump())
        questions[question_pos] = updated_question
        return questions[question_pos]

    async def delete_question(self, question_id: int) -> bool:
        if question_pos := \
                next(filter(lambda x: x.id == question_id, questions)):
            questions.remove(question_pos)
            return True