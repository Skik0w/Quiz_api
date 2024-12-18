from typing import Iterable
from quizapi.core.domain.player import Player, PlayerIn
from quizapi.core.repositories.iplayer import IPlayerRepository
from quizapi.infrastructure.dto.playerdto import PlayerDTO
from quizapi.infrastructure.dto.tokendto import TokenDTO
from quizapi.infrastructure.services.iplayer import IPlayerService
from pydantic import UUID4
from quizapi.infrastructure.utils.password import verify_password
from quizapi.infrastructure.utils.token import generate_player_token

class PlayerService(IPlayerService):

    _repository: IPlayerRepository

    def __init__(self, repository: IPlayerRepository):
        self._repository = repository

    async def register_player(self, player: PlayerIn) -> PlayerDTO | None:
        return await self._repository.register_player(player)

    async def authenticate_player(self, player: PlayerIn) -> TokenDTO | None:

        if player_data := await self._repository.get_player_by_email(player.email):
            if verify_password(player.password, player_data.password):
                token_details = generate_player_token(player_data.id)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)
            return None
        return None

    async def get_player_by_uuid(self, uuid: UUID4) -> PlayerDTO | None:
        return await self._repository.get_player_by_uuid(uuid)

    async def get_player_by_email(self, email: str) -> PlayerDTO | None:
        return await self._repository.get_player_by_email(email)