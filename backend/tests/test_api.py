from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_viewer_cannot_query_ai():
    response = client.post(
        "/ask-ai",
        json={"question": "Why did payment service fail?", "role": "Viewer", "user_id": "test-user"},
    )
    assert response.status_code == 403
