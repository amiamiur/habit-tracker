from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_habits_unauthorized():
    response = client.get("/habits/")
    assert response.status_code == 401
