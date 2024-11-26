from abc import ABC, abstractmethod
from typing import Iterable
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.core.domain.store import Reward, RewardIn

class IPlayerService(ABC):

    @abstractmethod
    async def get_player_by_id(self, player_id: int) -> Player | None:
        """ """

    @abstractmethod
    async def get_player_by_name(self, name: str) -> Player | None:
        """ """

    @abstractmethod
    async def get_all_players(self) -> Iterable[Player]:
        """ """

    @abstractmethod
    async def add_player(self, player: PlayerIn) -> None:
        """ """

    @abstractmethod
    async def update_player(self, player_id: int, player: PlayerIn) -> Player | None:
        """ """

    @abstractmethod
    async def delete_player(self, player_id: int) -> bool:
        """ """

    @abstractmethod
    async def get_player_rewards(self, player_id: int) -> Iterable[Reward]:
        """ """
