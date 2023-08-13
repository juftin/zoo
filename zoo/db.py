"""
Database Connections
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from zoo.config import config

engine = create_async_engine(config.connection_string, echo=config.DEBUG, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=False
)


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
