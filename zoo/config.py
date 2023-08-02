"""
Application configuration
"""

import logging
import pathlib
from typing import Optional

import fastapi
import starlette
import uvicorn
from pydantic import BaseSettings
from rich.logging import RichHandler
from sqlalchemy.engine import URL


class ZooSettings(BaseSettings):
    """
    Application configuration
    """

    PRODUCTION: bool = False
    DOCKER: bool = False

    DATABASE_FILE: str = str(pathlib.Path(__file__).resolve().parent / "zoo.sqlite")
    DATABASE_DRIVER: str = "sqlite+aiosqlite"
    DATABASE_HOST: Optional[str] = None
    DATABASE_PORT: Optional[int] = None
    DATABASE_USER: Optional[str] = None
    DATABASE_PASSWORD: Optional[str] = None
    DATABASE_NAME: Optional[str] = None

    class Config:
        """
        Pydantic configuration
        """

        env_prefix = "ZOO_"
        case_sensitive = True

    @property
    def connection_string(self) -> str:
        """
        Get the database connection string
        """
        database_url = str(
            URL.create(
                drivername=self.DATABASE_DRIVER,
                username=self.DATABASE_USER,
                password=self.DATABASE_PASSWORD,
                host=self.DATABASE_HOST or self.DATABASE_FILE,
                port=self.DATABASE_PORT,
                database=self.DATABASE_NAME,
            )
        )
        if all([self.DATABASE_HOST is None, "sqlite" in self.DATABASE_DRIVER.lower(), "////" not in database_url]):
            database_url = str(database_url).replace("///", "////", 1)
        return database_url

    @classmethod
    def debug_logging(cls) -> None:
        """
        Configure logging for development
        """
        for logger in logging.Logger.manager.loggerDict.values():
            if isinstance(logger, logging.Logger):
                if logger.handlers:
                    logger.handlers = [
                        RichHandler(
                            rich_tracebacks=True,
                            tracebacks_show_locals=True,
                            show_time=True,
                            omit_repeated_times=False,
                            tracebacks_suppress=[
                                starlette,
                                fastapi,
                                uvicorn,
                            ],
                        )
                    ]


config = ZooSettings()
