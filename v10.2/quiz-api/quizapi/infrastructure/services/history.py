from typing import Iterable
from quizapi.core.domain.history import History, HistoryIn
from quizapi.core.repositories.ihistory import IHistoryRepository
from quizapi.infrastructure.dto.historydto import HistoryDTO
from quizapi.infrastructure.dto.questiondto import QuestionDTO
from quizapi.infrastructure.services.ihistory import IHistoryService

from pydantic import UUID4

class HistoryService(IHistoryService):

    _repository: IHistoryRepository

    def __init__(self, repository: IHistoryRepository):

        self._repository = repository

    async def get_all_histories(self) -> Iterable[HistoryDTO]:
        return await self._repository.get_all_histories()

    async def get_history_by_id(self, history_id: int) -> HistoryDTO | None:
        return await self._repository.get_history_by_id(history_id)

    async def get_history_by_player(self, player_id: UUID4) -> Iterable[HistoryDTO] | None:
        return await self._repository.get_history_by_player(player_id)

    async def add_history(self, data: HistoryIn) -> History | None:
        total_questions = await self._repository.get_total_questions_by_quiz(data.quiz_id)
        total_questions = len(list(total_questions))
        if total_questions > 0:
            effectiveness = data.correct_answers / total_questions
            return await self._repository.add_history(
                data=data,
                total_questions=total_questions,
                effectiveness=effectiveness,
            )
        return None

    async def update_history(
            self,
            history_id: int,
            data: HistoryIn
    ) -> History | None:
        existing_history = await self._repository.get_history_by_id(history_id)
        if not existing_history:
            return None

        total_questions = await self._repository.get_total_questions_by_quiz(data.quiz_id)
        total_questions_count = len(list(total_questions))
        effectiveness = data.correct_answers / total_questions_count if total_questions_count > 0 else 0.0

        updated = await self._repository.update_history(
            history_id=history_id,
            data=data,
            total_questions=total_questions_count,
            effectiveness=effectiveness,
        )
        return updated

    async def delete_history(self, history_id: int) -> bool:
        return await self._repository.delete_history(history_id)

    async def get_total_questions_by_quiz(self, quiz_id: int) -> Iterable[QuestionDTO] | None:
        return await self._repository.get_total_questions_by_quiz(quiz_id)