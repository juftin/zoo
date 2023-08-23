"""
Test the Auth API
"""

from fastapi.testclient import TestClient


def test_get_access_token(migrated_client: TestClient) -> None:
    """
    Test POST /auth/jwt/login
    """
    response = migrated_client.post(
        "/auth/jwt/login",
        data={"username": "test@testing.com", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert len(token) == 43


def test_get_cookie(migrated_client: TestClient) -> None:
    """
    Test POST /auth/cookie/login
    """
    response = migrated_client.post(
        "/auth/cookie/login",
        data={"username": "test@testing.com", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 204
    assert "zoo-auth" in response.cookies
    assert len(response.cookies["zoo-auth"]) == 181
