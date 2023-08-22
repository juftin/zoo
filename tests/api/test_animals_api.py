"""
API Tests: /animals
"""

import datetime

from fastapi.testclient import TestClient

from zoo.schemas.animals import AnimalsRead


def test_get_animal(client: TestClient) -> None:
    """
    Test GET /animals
    """
    response = client.get("/animals")
    assert response.status_code == 200
    response_data = response.json()
    first_animal = AnimalsRead(**response_data[0])
    assert isinstance(first_animal.updated_at, datetime.datetime)
