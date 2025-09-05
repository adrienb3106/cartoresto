import pytest
from fastapi.testclient import TestClient
from backend.main import app
import backend.crud as crud

client = TestClient(app)

@pytest.fixture(autouse=True)
def fake_delete(monkeypatch):
    def fake_delete_restaurant(db, resto_id):
        return resto_id == 1
    monkeypatch.setattr(crud, "delete_restaurant", fake_delete_restaurant)

def test_delete_restaurant():
    response = client.delete("/restaurants/1")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
