"""
Test cases for the Staff API.
"""

import datetime
from os import environ

from fastapi.testclient import TestClient

from zoo.schemas.staff import StaffCreate, StaffRead, StaffUpdate


def test_get_staff_members(migrated_client: TestClient) -> None:
    """
    Test GET /staff
    """
    response = migrated_client.get("/staff")
    assert response.status_code == 200
    first_staff = StaffRead(**response.json()[0])
    assert isinstance(first_staff.updated_at, datetime.datetime)


def test_get_staff(migrated_client: TestClient) -> None:
    """
    Test GET /staff/{staff_id}
    """
    response = migrated_client.get("/staff/1")
    assert response.status_code == 200
    first_staff = StaffRead(**response.json())
    assert isinstance(first_staff.updated_at, datetime.datetime)


def test_get_staff_failure(migrated_client: TestClient) -> None:
    """
    Test GET /staff/{staff_id} - failure
    """
    response = migrated_client.get("/staff/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Error: `Staff` data not found or deleted - ID: 100"}


def test_create_staff(migrated_client: TestClient) -> None:
    """
    Test POST /staff
    """
    test_name = environ["PYTEST_CURRENT_TEST"].split(":")[-1].split(" ")[0]
    staff_body = StaffCreate(
        name=test_name,
        notes="test",
    )
    response = migrated_client.post(
        "/staff",
        json=staff_body.model_dump(exclude_unset=True),
    )
    assert response.status_code == 200
    response_data = response.json()
    staff = StaffRead(**response_data)
    assert staff.name == test_name
    assert staff.notes == "test"


def test_update_staff(migrated_client: TestClient) -> None:
    """
    Test PATCH /staff/{staff_id}
    """
    test_name = environ["PYTEST_CURRENT_TEST"].split(":")[-1].split(" ")[0]
    staff_body = StaffUpdate(
        notes=test_name,
    )
    response = migrated_client.patch(
        "/staff/1",
        json=staff_body.model_dump(exclude_unset=True),
    )
    assert response.status_code == 200
    response_data = response.json()
    staff = StaffRead(**response_data)
    assert staff.notes == test_name
