"""
User Database Model
"""

import asyncio
import contextlib
import uuid
from typing import AsyncGenerator

from fastapi import Depends, FastAPI
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from sqlalchemy.ext.asyncio import AsyncSession

from zoo._version import __application__
from zoo.config import app_config
from zoo.db import get_async_session
from zoo.models.base import Base, CreatedUpdatedMixin, UpdatedAtMixin
from zoo.schemas.users import UserCreate, UserRead

auth_endpoint = "auth"
jwt_endpoint = "jwt"
cookie_endpoint = "cookie"


class User(SQLAlchemyBaseUserTableUUID, CreatedUpdatedMixin, Base):
    """
    FastAPI Users - User Model
    """


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, UpdatedAtMixin, Base):
    """
    FastAPI Users - Access Token Model
    """

    __tablename__ = "access_token"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
    UserManager for FastAPI Users
    """


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Yield a SQLModelUserDatabaseAsync
    """
    yield SQLAlchemyUserDatabase(user_table=User, session=session)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyAccessTokenDatabase[AccessToken], None]:
    """
    Yield a SQLAlchemyAccessTokenDatabase
    """
    yield SQLAlchemyAccessTokenDatabase[AccessToken](
        access_token_table=AccessToken, session=session
    )


async def get_user_manager(user_db=Depends(get_user_db)) -> AsyncGenerator[UserManager, None]:
    """
    Yield a UserManager
    """
    yield UserManager(user_db=user_db)


def get_jwt_strategy() -> JWTStrategy:
    """
    Get a DatabaseStrategy using the AccessTokenDatabase
    """
    return JWTStrategy(
        secret=app_config.DATABASE_SECRET, lifetime_seconds=app_config.JWT_EXPIRATION
    )


def get_database_strategy(
    access_token_db: AccessTokenDatabase = Depends(get_access_token_db),
) -> DatabaseStrategy:
    """
    Get a DatabaseStrategy using the AccessTokenDatabase
    """
    return DatabaseStrategy(database=access_token_db, lifetime_seconds=app_config.JWT_EXPIRATION)


bearer_transport = BearerTransport(tokenUrl=f"{auth_endpoint}/{jwt_endpoint}/login")
cookie_transport = CookieTransport(cookie_name=f"{__application__}-auth", cookie_max_age=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
cookie_auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend, cookie_auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, *, is_superuser: bool = False) -> User:
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
                    UserCreate(email=email, password=password, is_superuser=is_superuser)
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
        fastapi_users.get_auth_router(auth_backend),
        prefix=f"/{auth_endpoint}/{jwt_endpoint}",
        tags=[auth_endpoint],
    )
    app.include_router(
        fastapi_users.get_auth_router(cookie_auth_backend),
        prefix=f"/{auth_endpoint}/{cookie_endpoint}",
        tags=[auth_endpoint],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix=f"/{auth_endpoint}",
        tags=[auth_endpoint],
    )
    # Skipping Routers:
    # - fastapi_users.get_reset_password_router()
    # - fastapi_users.get_verify_router(UserRead)
    # - fastapi_users.get_users_router(UserRead, UserUpdate)


if __name__ == "__main__":
    asyncio.run(
        create_user(
            email="admin@test.com",
            password="admin",
            is_superuser=True,
        )
    )
