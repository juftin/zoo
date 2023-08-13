"""
Test fixtures for the project.
"""

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from zoo.app import app as fastapi_app


@pytest.fixture
def app() -> FastAPI:
    """
    FastAPI application for testing.
    """
    return fastapi_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """
    Test client for FastAPI.
    """
    return TestClient(app)
