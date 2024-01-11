"""
Application configuration
"""

import asyncio
import logging
import pathlib
from typing import List, Optional, Union

import fastapi
import starlette
import uvicorn
from fastapi.routing import APIRoute
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.logging import RichHandler
from sqlalchemy.engine import URL

from zoo._version import __application__

rich_handler = RichHandler(
    rich_tracebacks=True,
    tracebacks_show_locals=True,
    show_time=True,
    omit_repeated_times=False,
    tracebacks_suppress=[
        starlette,
        fastapi,
        uvicorn,
        asyncio,
    ],
    log_time_format="[%Y-%m-%d %H:%M:%S]",
)


class ZooSettings(BaseSettings):
    """
    Application configuration
    """

    PRODUCTION: bool = False
    DOCKER: bool = False
    DEBUG: bool = False

    DATABASE_FILE: str = str(pathlib.Path(__file__).resolve().parent / "zoo.sqlite")
    DATABASE_DRIVER: str = "sqlite+aiosqlite"
    DATABASE_HOST: Optional[str] = None
    DATABASE_PORT: Optional[int] = None
    DATABASE_USER: Optional[str] = None
    DATABASE_PASSWORD: Optional[str] = None
    DATABASE_NAME: Optional[str] = None
    JWT_EXPIRATION: Optional[int] = None
    SEED_DATA: bool = True

    DATABASE_SECRET: str = __application__

    model_config = SettingsConfigDict(
        env_prefix="ZOO_",
        case_sensitive=True,
    )

    @property
    def connection_string(self) -> str:
        """
        Get the database connection string
        """
        database_url = URL.create(
            drivername=self.DATABASE_DRIVER,
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST or self.DATABASE_FILE,
            port=self.DATABASE_PORT,
            database=self.DATABASE_NAME,
        ).render_as_string(hide_password=False)
        if all(
            [
                self.DATABASE_HOST is None,
                "sqlite" in self.DATABASE_DRIVER.lower(),
                "////" not in database_url,
            ]
        ):
            database_url = str(database_url).replace("///", "////", 1)
        return database_url

    @classmethod
    def rich_logging(cls, loggers: List[Union[str, logging.Logger]]) -> None:
        """
        Configure logging for development
        """
        for logger in loggers:
            if isinstance(logger, str):
                logger_inst = logging.getLogger(logger)
            else:
                logger_inst = logger
            logger_inst.handlers = [rich_handler]

    @classmethod
    def custom_generate_unique_id(cls, route: APIRoute) -> str:
        """
        Custom function to generate unique id for each route
        """
        return f"{route.tags[0]}-{route.name}"


app_config = ZooSettings()
