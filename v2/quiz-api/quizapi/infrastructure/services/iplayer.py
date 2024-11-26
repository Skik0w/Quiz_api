from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.player import Player, PlayerIn

class IPlayerService(ABC):

    @abstractmethod
    async def get_player_by_id(self, player_id: int) -> Player | None:
        """ """

    @abstractmethod
    async def get_all_players(self) -> Iterable[Player]:
        """ """

    @abstractmethod
    async def add_player(self, data: PlayerIn) -> None:
        """ """

    @abstractmethod
    async def update_player(
            self,
            player_id: int,
            data: PlayerIn
    ) -> Player | None:
        """ """

    @abstractmethod
    async def delete_player(self, player_id: int) -> bool:
        """ """