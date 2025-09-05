import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.database import Base
from backend import models, schemas, crud

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_and_read_restaurant(db):
    resto_data = schemas.Restaurant(
        nom="Chez Adrien",
        adresse="123 rue X",
        localisation=schemas.Localisation(ville="Paris", code_postal="75000", pays="France"),
        informations=schemas.Informations(category="Italien", note=5, description="Super pasta")
    )

    db_resto = crud.create_restaurant(db, resto_data)
    assert db_resto.nom == "Chez Adrien"
    assert db_resto.localisation.ville == "Paris"
    assert db_resto.informations.note == 5

    restos = crud.get_restaurants(db)
    assert len(restos) == 1

def test_update_restaurant(db):
    resto_data = schemas.Restaurant(
        nom="Chez Luigi",
        adresse="456 rue Y",
        localisation=schemas.Localisation(ville="Lyon"),
        informations=schemas.Informations(category="Pizza", note=3)
    )
    db_resto = crud.create_restaurant(db, resto_data)

    updated = crud.update_restaurant(db, db_resto.id, {
        "nom": "Chez Luigi Updated",
        "localisation": {"ville": "Marseille"},
        "informations": {"note": 4}
    })
    assert updated.nom == "Chez Luigi Updated"
    assert updated.localisation.ville == "Marseille"
    assert updated.informations.note == 4

def test_delete_restaurant(db):
    resto_data = schemas.Restaurant(
        nom="Chez Mario",
        adresse="789 rue Z",
        localisation=schemas.Localisation(ville="Nice"),
        informations=schemas.Informations(category="Burger", note=2)
    )
    db_resto = crud.create_restaurant(db, resto_data)

    success = crud.delete_restaurant(db, db_resto.id)
    assert success is True
    assert crud.get_restaurant(db, db_resto.id) is None
