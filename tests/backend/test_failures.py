"""
API Tests: /animals
"""

from fastapi.testclient import TestClient


def test_get_bad_endpoint(client: TestClient) -> None:
    """
    Return a bad response for unexpected endpoint
    """
    response = client.get("/badEndpoint")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
