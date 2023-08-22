"""
API Tests: /animals
"""

import datetime
from os import environ

from fastapi.testclient import TestClient

from zoo.schemas.animals import AnimalsCreate, AnimalsRead, AnimalsUpdate


def test_get_animals(client: TestClient) -> None:
    """
    Test GET /animals
    """
    response = client.get("/animals")
    assert response.status_code == 200
    response_data = response.json()
    first_animal = AnimalsRead(**response_data[0])
    assert isinstance(first_animal.updated_at, datetime.datetime)


def test_get_animal(client: TestClient) -> None:
    """
    Test GET /animals/{animal_id}
    """
    response = client.get("/animals/1")
    assert response.status_code == 200
    response_data = response.json()
    first_animal = AnimalsRead(**response_data)
    assert isinstance(first_animal.updated_at, datetime.datetime)


def test_get_animal_failure(client: TestClient) -> None:
    """
    Test GET /animals/{animal_id} - failure
    """
    response = client.get("/animals/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Error: `Animals` data not found or deleted - ID: 100"}


def test_create_animal(client: TestClient) -> None:
    """
    Test POST /animals
    """
    test_name = environ["PYTEST_CURRENT_TEST"].split(":")[-1].split(" ")[0]
    animal_body = AnimalsCreate(
        name=test_name,
        description="test",
    )
    response = client.post(
        "/animals",
        json=animal_body.model_dump(exclude_unset=True),
    )
    assert response.status_code == 200
    response_data = response.json()
    animal = AnimalsRead(**response_data)
    assert animal.name == test_name
    assert animal.description == "test"


def test_update_animal(client: TestClient) -> None:
    """
    Test POST /animals/{animal_id}
    """
    test_name = environ["PYTEST_CURRENT_TEST"].split(":")[-1].split(" ")[0]
    animal_body = AnimalsUpdate(
        description=test_name,
    )
    response = client.patch(
        "/animals/2",
        json=animal_body.model_dump(exclude_unset=True),
    )
    # assert response.status_code == 200
    response_data = response.json()
    animal = AnimalsRead(**response_data)
    assert animal.description == test_name


def test_delete_animal(client: TestClient) -> None:
    """
    Test DELETE /animals/{animal_id}
    """
    response = client.delete("/animals/5")
    assert response.status_code == 200
    response_data = response.json()
    animal = AnimalsRead(**response_data)
    assert animal.deleted_at is not None
