"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from quizapi.infrastructure.repositories.quizdb import \
    QuizRepository
from quizapi.infrastructure.repositories.questiondb import \
    QuestionRepository
from quizapi.infrastructure.repositories.playerdb import \
    PlayerRepository
from quizapi.infrastructure.repositories.historydb import \
    HistoryRepository
from quizapi.infrastructure.repositories.tournamentdb import \
    TournamentRepository
from quizapi.infrastructure.repositories.rewarddb import \
    RewardRepository
from quizapi.infrastructure.repositories.shopdb import \
    ShopRepository

from quizapi.infrastructure.services.quiz import QuizService
from quizapi.infrastructure.services.question import QuestionService
from quizapi.infrastructure.services.player import PlayerService
from quizapi.infrastructure.services.history import HistoryService
from quizapi.infrastructure.services.tournament import TournamentService
from quizapi.infrastructure.services.reward import RewardService
from quizapi.infrastructure.services.shop import ShopService

class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    quiz_repository = Singleton(QuizRepository)
    question_repository = Singleton(QuestionRepository)
    player_repository = Singleton(PlayerRepository)
    history_repository = Singleton(HistoryRepository)
    tournament_repository = Singleton(TournamentRepository)
    reward_repository = Singleton(RewardRepository)
    shop_repository = Singleton(ShopRepository)

    quiz_service = Factory(
        QuizService,
        repository=quiz_repository,
    )
    question_service = Factory(
        QuestionService,
        repository=question_repository,
    )
    player_service = Factory(
        PlayerService,
        repository=player_repository,
    )
    history_service = Factory(
        HistoryService,
        repository=history_repository,
    )
    tournament_service = Factory(
        TournamentService,
        repository=tournament_repository,
    )
    reward_service = Factory(
        RewardService,
        repository=reward_repository,
    )
    shop_service = Factory(
        ShopService,
        repository=shop_repository,
    )