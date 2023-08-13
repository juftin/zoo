"""
API Tests: /animals
"""

import datetime

from fastapi.testclient import TestClient

from zoo.models import Animals


def test_get_animal(client: TestClient) -> None:
    """
    Test GET /animals
    """
    response = client.get("/animals")
    assert response.status_code == 200
    response_data = response.json()
    first_animal = Animals(**response_data[0])
    assert isinstance(first_animal.modified_at, datetime.datetime)
