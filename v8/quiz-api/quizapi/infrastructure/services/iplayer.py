from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.infrastructure.dto.playerdto import PlayerDTO
from quizapi.infrastructure.dto.tokendto import TokenDTO
from pydantic import UUID5

class IPlayerService(ABC):

    @abstractmethod
    async def register_player(self, player: PlayerIn) -> PlayerDTO | None:
        """ """

    @abstractmethod
    async def authenticate_player(self, player: PlayerIn) -> TokenDTO | None:
        """ """

    @abstractmethod
    async def get_player_by_uuid(self, uuid: UUID5) -> PlayerDTO | None:
        """ """

    async def get_player_by_email(self, email: str) -> PlayerDTO | None:
        """ """