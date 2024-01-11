"""
Test fixtures for the project.
"""

import pathlib
from tempfile import TemporaryDirectory
from typing import Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

from zoo.config import app_config


@pytest.fixture(scope="session")
def migrated_client() -> Generator[TestClient, None, None]:
    """
    Test client for the FastAPI app with a shared temporary database.

    This fixture is session-scoped, so it will only be created once for
    the entire test session. It creates a temporary directory and database
    file, and runs the Alembic migrations to set up the database schema.
    It then imports the FastAPI app and returns a test client for it.
    """
    with pytest.MonkeyPatch.context() as monkeypatch, TemporaryDirectory() as temp_dir:
        # Create a temporary database file and update the config
        temp_path = pathlib.Path(temp_dir)
        temp_db = temp_path / "zoo.sqlite"
        monkeypatch.setattr(target=app_config, name="DATABASE_FILE", value=str(temp_db))
        monkeypatch.setenv("ZOO_DATABASE_FILE", str(temp_db))
        # Set the seed data flag to True
        monkeypatch.setattr(target=app_config, name="SEED_DATA", value=True)
        monkeypatch.setenv("ZOO_SEED_DATA", "True")
        # Change directory to the root of the project
        zoo_dir = pathlib.Path(__file__).parent.parent
        monkeypatch.chdir(zoo_dir)
        # Run migrations before importing app
        config = Config(zoo_dir / "alembic.ini")
        command.upgrade(config, "head")
        # Import app after monkeypatching
        from zoo.app import app as fastapi_app

        # Return the test client
        yield TestClient(fastapi_app)
