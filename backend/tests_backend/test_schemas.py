import pytest
from pydantic import ValidationError
from backend import schemas


def test_restaurant_schema_valid_full():
    """Un JSON complet et valide doit être accepté et toutes les infos doivent être accessibles"""
    data = {
        "nom": "Chez Adrien",
        "adresse": "123 rue X",
        "localisation": {
            "ville": "Paris",
            "code_postal": "75000",
            "pays": "France",
            "latitude": 48.8566,
            "longitude": 2.3522
        },
        "informations": {
            "category": "Italien",
            "note": 5,
            "description": "Super pasta",
            "review": "Top service"
        }
    }

    resto = schemas.Restaurant(**data)

    # Vérification des champs Restaurant
    assert resto.nom == "Chez Adrien"
    assert resto.adresse == "123 rue X"

    # Vérification des champs Localisation
    assert resto.localisation.ville == "Paris"
    assert resto.localisation.code_postal == "75000"
    assert resto.localisation.pays == "France"
    assert resto.localisation.latitude == 48.8566
    assert resto.localisation.longitude == 2.3522

    # Vérification des champs Informations
    assert resto.informations.category == "Italien"
    assert resto.informations.note == 5
    assert resto.informations.description == "Super pasta"
    assert resto.informations.review == "Top service"


def test_restaurant_schema_invalid_nom():
    """Le champ nom doit être une string"""
    data = {
        "nom": 12345,  # invalide
        "localisation": {"ville": "Paris"},
        "informations": {"category": "Italien"}
    }
    with pytest.raises(ValidationError):
        schemas.Restaurant(**data)


def test_localisation_schema_missing_required_field():
    """Le champ ville est obligatoire dans Localisation"""
    data = {
        "code_postal": "75000",
        "pays": "France"
    }
    with pytest.raises(ValidationError):
        schemas.Localisation(**data)


def test_informations_schema_valid():
    """Test complet pour Informations"""
    data = {
        "category": "Asiatique",
        "note": 4,
        "description": "Pho excellent",
        "review": "Bon service"
    }

    info = schemas.Informations(**data)

    assert info.category == "Asiatique"
    assert info.note == 4
    assert info.description == "Pho excellent"
    assert info.review == "Bon service"
