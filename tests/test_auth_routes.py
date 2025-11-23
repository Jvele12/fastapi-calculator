from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login_flow():
    payload = {
        "username": "route_user",
        "email": "route_user@example.com",
        "password": "pw123",
    }

    r = client.post("/users/register", json=payload)
    assert r.status_code in (200, 400)

    login_payload = {"email": payload["email"], "password": payload["password"]}
    r2 = client.post("/users/login", json=login_payload)
    assert r2.status_code == 200
    data = r2.json()
    assert data["email"] == payload["email"]
