from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_calculation_bread_flow():
    create_payload = {"a": 6, "b": 3, "type": "divide"}
    r = client.post("/calculations", json=create_payload)
    assert r.status_code == 201
    calc = r.json()
    calc_id = calc["id"]
    assert calc["result"] == 2.0

    r_list = client.get("/calculations")
    assert r_list.status_code == 200
    assert any(c["id"] == calc_id for c in r_list.json())

    r_get = client.get(f"/calculations/{calc_id}")
    assert r_get.status_code == 200
    assert r_get.json()["id"] == calc_id

    update_payload = {"a": 10, "b": 5}
    r_put = client.put(f"/calculations/{calc_id}", json=update_payload)
    assert r_put.status_code == 200
    updated = r_put.json()
    assert updated["result"] == 2.0  # 10 / 5

    r_del = client.delete(f"/calculations/{calc_id}")
    assert r_del.status_code == 204

    r_get2 = client.get(f"/calculations/{calc_id}")
    assert r_get2.status_code == 404


def test_divide_by_zero_route_rejected():
    payload = {"a": 1, "b": 0, "type": "divide"}
    r = client.post("/calculations", json=payload)
    assert r.status_code == 422
