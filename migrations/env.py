"""
Alembic migration environment.
"""

import asyncio
import logging
from logging.config import fileConfig
from os import getenv

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from zoo.config import app_config
from zoo.models import __all_models__
from zoo.models.base import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Register all Database Models with Alembic
known_models = __all_models__
target_metadata = Base.metadata

if not app_config.DOCKER and getenv("PYTEST_CURRENT_TEST", None) is None:  # pragma: no cover
    app_config.rich_logging(loggers=[logging.getLogger()])


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = app_config.connection_string
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def sync_run_migrations(connection):
    """
    Run migrations in 'sync' mode.
    """
    context.configure(connection=connection, target_metadata=target_metadata, include_schemas=True)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # raise ValueError(app_config.connection_string)
    engine = create_async_engine(app_config.connection_string, echo=app_config.DEBUG, future=True)
    async with engine.connect() as connection:
        await connection.run_sync(sync_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
