import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)
from quizapi.config import config

metadata = sqlalchemy.MetaData()

player_table = sqlalchemy.Table(
    "players",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()")
    ),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

quiz_table = sqlalchemy.Table(
    "quizzes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column(
        "player_id",
        sqlalchemy.ForeignKey("players.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "player_username",
        sqlalchemy.ForeignKey("players.username"),
        nullable=False,
    ),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("shared", sqlalchemy.Boolean),
)

question_table = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("option_one", sqlalchemy.String),
    sqlalchemy.Column("option_two", sqlalchemy.String),
    sqlalchemy.Column("option_three", sqlalchemy.String),
    sqlalchemy.Column("option_four", sqlalchemy.String),
    sqlalchemy.Column("correct_answer", sqlalchemy.String),
    sqlalchemy.Column(
        "quiz_id",
        sqlalchemy.ForeignKey("quizzes.id"),
        nullable=False,
    )
)

history_table = sqlalchemy.Table(
    "history",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "player_id",
        sqlalchemy.ForeignKey("players.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "quiz_id",
        sqlalchemy.ForeignKey("quizzes.id"),
    ),
    sqlalchemy.Column("total_questions", sqlalchemy.Integer),
    sqlalchemy.Column("correct_answers", sqlalchemy.Integer),
    sqlalchemy.Column("effectiveness", sqlalchemy.Float),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime(timezone=True)),
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:

    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")