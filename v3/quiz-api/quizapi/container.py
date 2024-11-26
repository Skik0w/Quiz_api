from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from quizapi.infrastructure.repositories.quizmock import \
    QuizMockRepository
from quizapi.infrastructure.repositories.questionmock import \
    QuestionMockRepository
from quizapi.infrastructure.repositories.playermock import \
    PlayerMockRepository
from quizapi.infrastructure.services.quiz import QuizService
from quizapi.infrastructure.services.question import QuestionService
from quizapi.infrastructure.services.player import PlayerService

class Container(DeclarativeContainer):

    quiz_repository = Singleton(QuizMockRepository)
    question_repository = Singleton(QuestionMockRepository)
    player_repository = Singleton(PlayerMockRepository)

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