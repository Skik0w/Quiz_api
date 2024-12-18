from abc import ABC, abstractmethod
from typing import Any, Iterable
from quizapi.core.domain.player import PlayerIn
from pydantic import UUID5

class IPlayerRepository(ABC):

    @abstractmethod
    async def get_player_by_uuid(self, uuid: UUID5) -> Any | None:
        """ """

    async def get_player_by_email(self, email: str) -> Any | None:
        """"""

    async def register_player(self, player: PlayerIn) -> Any | None:
        """"""