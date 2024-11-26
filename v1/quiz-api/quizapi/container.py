from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from quizapi.infrastructure.repositories.quizmock import \
    QuizMockRepository
from quizapi.infrastructure.repositories.questionmock import \
    QuestionMockRepository
from quizapi.infrastructure.repositories.storemock import \
    StoreMockRepository
from quizapi.infrastructure.repositories.playermock import \
    PlayerMockRepository
from quizapi.infrastructure.repositories.gamehistorymock import \
    GameHistoryMockRepository
from quizapi.infrastructure.services.quiz import QuizService
from quizapi.infrastructure.services.question import QuestionService
from quizapi.infrastructure.services.store import StoreService
from quizapi.infrastructure.services.player import PlayerService
from quizapi.infrastructure.services.gamehistory import GameHistoryService


class Container(DeclarativeContainer):
    quiz_repository = Singleton(QuizMockRepository)
    question_repository = Singleton(QuestionMockRepository)
    store_repository = Singleton(StoreMockRepository)
    player_repository = Singleton(PlayerMockRepository)
    game_history_repository = Singleton(GameHistoryMockRepository)

    quiz_service = Factory(
        QuizService,
        repository=quiz_repository,
    )
    question_service = Factory(
        QuestionService,
        repository=quiz_repository,
    )
    store_service = Factory(
        StoreService,
        repository=store_repository,
    )
    player_service = Factory(
        PlayerService,
        repository=player_repository,
    )
    game_history_service = Factory(
        GameHistoryService,
        repository=game_history_repository,
    )