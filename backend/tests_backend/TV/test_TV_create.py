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
def fake_create(monkeypatch):
    def fake_create_restaurant(db, resto):
        return FAKE_RESTAURANT
    monkeypatch.setattr(crud, "create_restaurant", fake_create_restaurant)

def test_create_restaurant():
    response = client.post("/restaurants/", json={
        "nom": "Chez Adrien",
        "adresse": "42 rue de l'Univers",
        "localisation_id": 1,
        "informations_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Chez Adrien"
    assert data["localisation"]["ville"] == "Paris"
