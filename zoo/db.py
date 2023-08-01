"""
Database Connections
"""

import pathlib
from os import getenv
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

local_database_file = pathlib.Path(__file__).parent / "zoo.sqlite"
sqlite_url = f"sqlite+aiosqlite:///{local_database_file}"
database_url = getenv("DATABASE_URL", sqlite_url)

engine = create_async_engine(database_url, echo=True, future=True)


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
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
