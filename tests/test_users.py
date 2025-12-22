from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
