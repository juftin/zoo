"""
Database Connections
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from zoo.config import app_config

async_engine = create_async_engine(app_config.connection_string, echo=app_config.DEBUG, future=True)
async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an AsyncSession

    Used by FastAPI Depends
    """
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
