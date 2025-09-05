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
def fake_update(monkeypatch):
    def fake_update_restaurant(db, resto_id, resto):
        if resto_id == FAKE_RESTAURANT.id:
            return FAKE_RESTAURANT
        return None
    monkeypatch.setattr(crud, "update_restaurant", fake_update_restaurant)

def test_update_restaurant():
    response = client.put("/restaurants/1", json={
        "nom": "Chez Adrien",
        "adresse": "42 rue de l'Univers",
        "localisation_id": 1,
        "informations_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["nom"] == "Chez Adrien"

def test_update_restaurant_not_found():
    response = client.put("/restaurants/999", json={
        "nom": "Fantôme",
        "adresse": "Inconnue",
        "localisation_id": 1,
        "informations_id": 1
    })
    # Ton endpoint renvoie 404 si crud.update_restaurant retourne None
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Restaurant not found"