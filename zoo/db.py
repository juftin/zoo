"""
Database Connections
"""

from typing import AsyncGenerator

from sqlalchemy import Table
from sqlalchemy.event import listens_for
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import Connection
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from zoo.config import ZooSettings
from zoo.models.animals import Animals

config = ZooSettings()
engine = create_async_engine(config.connection_string, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=False)


@listens_for(Animals.__table__, "after_create")  # type: ignore[attr-defined]
def seed_animals_table(target: Table, connection: Connection, **kwargs) -> None:  # noqa: ARG001
    """
    Seed the Animals table with initial data
    """
    Animals.create_seed_data(target=target, connection=connection)


async def init_db() -> None:
    """
    Initialize the database
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an AsyncSession

    Used by FastAPI Depends
    """
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
