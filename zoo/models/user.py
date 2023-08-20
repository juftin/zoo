"""
FastAPI Users
"""

import asyncio
import contextlib
import logging
import uuid

from fastapi import Depends, FastAPI
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB, SQLModelUserDatabaseAsync
from fastapi_users_db_sqlmodel.access_token import (
    SQLModelAccessTokenDatabaseAsync,
    SQLModelBaseAccessToken,
)
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from zoo.config import config
from zoo.db import get_async_session
from zoo.models.base import CreatedModifiedMixin

logger = logging.getLogger(__name__)


class User(SQLModelBaseUserDB, CreatedModifiedMixin, table=True):
    """
    FastAPI Users - User Model
    """


class UserRead(schemas.BaseUser[uuid.UUID], CreatedModifiedMixin):  # type: ignore[misc]
    """
    FastAPI Users - User Read Model
    """


class UserCreate(schemas.BaseUserCreate):
    """
    FastAPI Users - User Create Model
    """


class UserUpdate(schemas.BaseUserUpdate):
    """
    FastAPI Users - User Update Model
    """


class AccessToken(SQLModelBaseAccessToken, table=True):
    """
    FastAPI Users - Access Token Model
    """

    __tablename__ = "access_token"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
    UserManager for FastAPI Users
    """

    reset_password_token_secret = config.DATABASE_SECRET
    verification_token_secret = config.DATABASE_SECRET


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Yield a SQLModelUserDatabaseAsync
    """
    yield SQLModelUserDatabaseAsync(user_model=User, session=session)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLModelAccessTokenDatabaseAsync[AccessToken](
        access_token_model=AccessToken, session=session
    )


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Yield a UserManager
    """
    yield UserManager(user_db=user_db)


def get_database_strategy(
    access_token_db: AccessTokenDatabase = Depends(get_access_token_db),
) -> DatabaseStrategy:
    """
    Get a DatabaseStrategy using the AccessTokenDatabase
    """
    return DatabaseStrategy(database=access_token_db, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager=get_user_manager, auth_backends=[auth_backend]
)

current_active_user = fastapi_users.current_user(active=True)


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str, password: str, is_superuser: bool = False  # noqa: FBT001, FBT002
) -> User:
    """
    Create a user

    Parameters
    ----------
    email: str
        User email
    password: str
        User password
    is_superuser: bool
        Is the user a superuser

    Returns
    -------
    User

    Raises
    ------
    UserAlreadyExists
        If the user already exists
    """
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.create(
                    UserCreate(email=EmailStr(email), password=password, is_superuser=is_superuser)
                )
                return user


def bootstrap_fastapi_users(app: FastAPI) -> None:
    """
    Bootstrap the application with FastAPI Users Routers

    Parameters
    ----------
    app: FastAPI

    Returns
    -------
    None
    """
    app.include_router(
        fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )


if __name__ == "__main__":
    asyncio.run(
        create_user(
            email="admin@test.com",
            password="admin",
            is_superuser=True,
        )
    )
