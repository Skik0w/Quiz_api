from abc import ABC, abstractmethod
from typing import Any, Iterable
from quizapi.core.domain.history import HistoryIn

class IHistoryRepository(ABC):

    @abstractmethod
    async def get_all_histories(self) -> Iterable[Any]:
        """ """

    @abstractmethod
    async def get_history_by_id(self, history_id: int) -> Any | None:
        """ """

    @abstractmethod
    async def get_history_by_player(self, player_id: int) -> Iterable[Any] | None:
        """ """

    @abstractmethod
    async def add_history(self, data: HistoryIn) -> Any | None:
        """ """

    @abstractmethod
    async def update_history(
            self,
            history_id: int,
            data: HistoryIn
    ) -> Any | None:
        """ """

    @abstractmethod
    async def delete_history(self, history_id: int) -> bool:
        """ """