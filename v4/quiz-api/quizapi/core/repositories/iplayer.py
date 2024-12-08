"""Module containing player repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from quizapi.core.domain.player import PlayerIn

class IPlayerRepository(ABC):

    @abstractmethod
    async def get_player_by_id(self, player_id: int) -> Any | None:
        """ """

    @abstractmethod
    async def get_all_players(self) -> Iterable[Any]:
        """ """

    @abstractmethod
    async def add_player(self, data: PlayerIn) -> Any | None:
        """ """

    @abstractmethod
    async def update_player(
            self,
            player_id: int,
            data: PlayerIn) -> Any | None:
        """ """

    @abstractmethod
    async def delete_player(self, player_id: int) -> bool:
        """ """