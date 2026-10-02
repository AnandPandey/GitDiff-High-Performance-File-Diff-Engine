from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "GitDiff API"
    }


def test_diff_api():
    response = client.post(
        "/api/diff",
        json={
            "old_text": "hello\nworld",
            "new_text": "hello\nbeautiful world"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["added"] == 1
    assert data["deleted"] == 1
    assert data["unchanged"] == 1