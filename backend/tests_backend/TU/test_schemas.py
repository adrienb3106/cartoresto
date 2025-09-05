import pytest
from backend import schemas


def test_schema_localisation():
    data = {
        "id": 1,
        "ville": "Paris",
        "code_postal": "75000",
        "pays": "France",
        "latitude": 48.8566,
        "longitude": 2.3522
    }
    loc = schemas.LocalisationRead(**data)
    assert loc.id == 1
    assert loc.ville == "Paris"
    assert loc.code_postal == "75000"
    assert loc.pays == "France"
    assert loc.latitude == 48.8566
    assert loc.longitude == 2.3522


def test_schema_informations():
    data = {
        "id": 1,
        "category": "Italien",
        "note": 5,
        "description": "Super pasta",
        "review": "Excellente ambiance"
    }
    infos = schemas.InformationsRead(**data)
    assert infos.id == 1
    assert infos.category == "Italien"
    assert infos.note == 5
    assert infos.description == "Super pasta"
    assert infos.review == "Excellente ambiance"


def test_schema_restaurant_complete():
    data = {
        "id": 1,
        "nom": "Chez Adrien",
        "adresse": "123 rue X",
        "localisation": {
            "id": 1,
            "ville": "Paris",
            "code_postal": "75000",
            "pays": "France"
        },
        "informations": {
            "id": 1,
            "category": "Italien",
            "note": 5,
            "description": "Super pasta"
        }
    }
    resto = schemas.RestaurantRead(**data)
    assert resto.id == 1
    assert resto.nom == "Chez Adrien"
    assert resto.adresse == "123 rue X"
    assert resto.localisation.ville == "Paris"
    assert resto.informations.category == "Italien"


def test_schema_restaurant_with_nulls():
    data = {
        "id": 2,
        "nom": "Chez Test",
        "adresse": "456 rue Y",
        "localisation": None,
        "informations": None
    }
    resto = schemas.RestaurantRead(**data)
    assert resto.id == 2
    assert resto.nom == "Chez Test"
    assert resto.adresse == "456 rue Y"
    assert resto.localisation is None
    assert resto.informations is None
