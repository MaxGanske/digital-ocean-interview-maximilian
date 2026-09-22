from fastapi.testclient import TestClient

from src.app.main import app


client = TestClient(app)


def test_create_short_url_is_scaffolded():
    response = client.post(
        "/api/shorten",
        json={
            "target_url": "https://example.com",
        },
    )

    assert response.status_code == 501