from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_profile_update_and_password_change_flow():
    # Use unique email to avoid collisions if DB persists
    email = "profile_test_unique@example.com"
    password = "password123"

    # Register
    r = client.post("/register", json={"username": "profiletest", "email": email, "password": password})
    assert r.status_code == 201
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # GET profile
    r = client.get("/profile", headers=headers)
    assert r.status_code == 200
    assert r.json()["email"] == email

    # Update username
    r = client.put("/profile", json={"username": "updatedname"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "updatedname"

    # Change password
    new_password = "newpass123"
    r = client.put("/profile/password", json={"current_password": password, "new_password": new_password}, headers=headers)
    assert r.status_code == 200
    assert r.json()["message"].lower().startswith("password updated")

    # Login with old password should fail
    r = client.post("/login", json={"email": email, "password": password})
    assert r.status_code == 401

    # Login with new password should succeed
    r = client.post("/login", json={"email": email, "password": new_password})
    assert r.status_code == 200
    assert "access_token" in r.json()
