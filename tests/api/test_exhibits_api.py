"""
Test cases for the Exhibits API.
"""

import datetime
from os import environ

from fastapi.testclient import TestClient

from zoo.schemas.exhibits import ExhibitsCreate, ExhibitsRead, ExhibitsUpdate
from zoo.schemas.staff import StaffRead


def test_get_exhibits(migrated_client: TestClient) -> None:
    """
    Test GET /exhibits
    """
    response = migrated_client.get("/exhibits")
    assert response.status_code == 200
    response_data = response.json()
    first_exhibit = ExhibitsRead(**response_data[0])
    assert isinstance(first_exhibit.updated_at, datetime.datetime)


def test_get_exhibit(migrated_client: TestClient) -> None:
    """
    Test GET /exhibits/{exhibit_id}
    """
    response = migrated_client.get("/exhibits/1")
    assert response.status_code == 200
    response_data = response.json()
    first_exhibit = ExhibitsRead(**response_data)
    assert isinstance(first_exhibit.updated_at, datetime.datetime)


def test_get_exhibit_failure(migrated_client: TestClient) -> None:
    """
    Test GET /exhibits/{exhibit_id} - failure
    """
    response = migrated_client.get("/exhibits/100")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Error: `Exhibits` data not found or deleted - ID: 100"
    }


def test_create_exhibit(migrated_client: TestClient) -> None:
    """
    Test POST /exhibits
    """
    test_name = environ["PYTEST_CURRENT_TEST"].split(":")[-1].split(" ")[0]
    exhibit_body = ExhibitsCreate(
        name=test_name,
        description="test",
    )
    response = migrated_client.post(
        "/exhibits",
        json=exhibit_body.model_dump(exclude_unset=True),
    )
    assert response.status_code == 200
    response_data = response.json()
    exhibit = ExhibitsRead(**response_data)
    assert exhibit.name == test_name


def test_update_exhibit(migrated_client: TestClient) -> None:
    """
    Test PATCH /exhibits/{exhibit_id}
    """
    test_name = environ["PYTEST_CURRENT_TEST"].split(":")[-1].split(" ")[0]
    exhibit_body = ExhibitsUpdate(
        description=test_name,
    )
    response = migrated_client.patch(
        "/exhibits/1",
        json=exhibit_body.model_dump(exclude_unset=True),
    )
    assert response.status_code == 200
    response_data = response.json()
    exhibit = ExhibitsRead(**response_data)
    assert exhibit.description == test_name


def test_delete_exhibit(migrated_client: TestClient) -> None:
    """
    Test DELETE /exhibits/{exhibit_id}
    """
    response = migrated_client.delete("/exhibits/2")
    assert response.status_code == 200
    response_data = response.json()
    exhibit = ExhibitsRead(**response_data)
    assert isinstance(exhibit.deleted_at, datetime.datetime)


def test_get_exhibit_staff(migrated_client: TestClient) -> None:
    """
    Test GET /exhibits/{exhibit_id}/staff
    """
    response = migrated_client.get("/exhibits/1/staff")
    assert response.status_code == 200
    first_staff = StaffRead(**response.json()[0])
    assert isinstance(first_staff.updated_at, datetime.datetime)
