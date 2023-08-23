"""
Utils Testing
"""

import datetime

from fastapi.testclient import TestClient

from zoo.schemas.utils import Health


def test_get_health(migrated_client: TestClient) -> None:
    """
    Test the health check endpoint
    """
    response = migrated_client.get("/health")
    assert response.status_code == 200
    health_response = Health(**response.json())
    assert health_response.status == "OK"
    assert health_response.code == 200
    assert isinstance(health_response.timestamp, datetime.datetime)


def test_swagger_docs(migrated_client: TestClient) -> None:
    """
    Test the swagger docs endpoint
    """
    response = migrated_client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
