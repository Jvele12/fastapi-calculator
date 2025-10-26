from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_endpoint():
    response = client.get("/add?a=3&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 5}
