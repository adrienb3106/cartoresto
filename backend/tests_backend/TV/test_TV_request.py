import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_restaurants():
    response = client.get("/restaurants/")
    
    # Vérifie que la requête a réussi
    assert response.status_code == 200
    
    data = response.json()
    
    # Vérifie que la réponse est une liste
    assert isinstance(data, list)
    
    # Vérifie qu'il y a bien au moins 1 restaurant (vu que ta BDD contient déjà des données)
    assert len(data) > 0
