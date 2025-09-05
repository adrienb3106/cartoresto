import pytest
from fastapi.testclient import TestClient
from backend.main import app
import backend.crud as crud
from backend import models

client = TestClient(app)

FAKE_RESTAURANT = models.Restaurant(
    id=1,
    nom="Chez Adrien",
    adresse="42 rue de l'Univers",
    localisation=models.Localisation(id=1, ville="Paris", code_postal="75000", pays="France"),
    informations=models.Informations(id=1, category="Français", note=5, description="Bistro sympa")
)

@pytest.fixture(autouse=True)
def fake_read(monkeypatch):
    def fake_read_restaurants(db, skip=0, limit=100):
        return [FAKE_RESTAURANT]
    monkeypatch.setattr(crud, "read_restaurants", fake_read_restaurants)

def test_read_restaurants():
    response = client.get("/restaurants/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["nom"] == "Chez Adrien"
