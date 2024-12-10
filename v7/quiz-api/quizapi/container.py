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
from quizapi.infrastructure.services.quiz import QuizService
from quizapi.infrastructure.services.question import QuestionService
from quizapi.infrastructure.services.player import PlayerService
from quizapi.infrastructure.services.history import HistoryService

class Container(DeclarativeContainer):

    quiz_repository = Singleton(QuizRepository)
    question_repository = Singleton(QuestionRepository)
    player_repository = Singleton(PlayerRepository)
    history_repository = Singleton(HistoryRepository)

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