"""
Database Connections
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from zoo.config import ZooSettings

config = ZooSettings()
engine = create_async_engine(config.connection_string, echo=True, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=False
)


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
