from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.history import History, HistoryIn
from quizapi.infrastructure.dto.historydto import HistoryDTO
from pydantic import UUID4


class IHistoryService(ABC):

    @abstractmethod
    async def get_all_histories(self) -> Iterable[HistoryDTO]:
        """ """

    @abstractmethod
    async def get_history_by_id(self, history_id: int) -> HistoryDTO | None:
        """ """

    @abstractmethod
    async def get_history_by_player(self, player_id: UUID4) -> Iterable[HistoryDTO] | None:
        """ """

    @abstractmethod
    async def add_history(self, data: HistoryIn) -> History | None:
        """ """

    @abstractmethod
    async def update_history(
            self,
            history_id: int,
            data: HistoryIn
    ) -> History | None:
        """ """

    @abstractmethod
    async def delete_history(self, history_id: int) -> bool:
        """ """

    @abstractmethod
    async def get_total_questions_by_quiz(self, quiz_id: int) -> int | None:
        """ """