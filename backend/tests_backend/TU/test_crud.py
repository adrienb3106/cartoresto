import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.core.database import Base
from backend import crud, schemas

# --- DB SQLite in-memory ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_and_read_restaurant(db):
    resto_in = schemas.RestaurantCreate(
        nom="Chez Adrien",
        adresse="123 rue X",
        localisation=schemas.LocalisationCreate(ville="Paris", code_postal="75000", pays="France"),
        informations=schemas.InformationsCreate(category="Italien", note=5, description="Super pasta")
    )

    resto = crud.create_restaurant(db, resto_in)
    assert resto.id is not None
    assert resto.nom == "Chez Adrien"
    assert resto.localisation.ville == "Paris"
    assert resto.informations.category == "Italien"

    fetched = crud.read_restaurant(db, resto.id)
    assert fetched.nom == "Chez Adrien"


def test_update_restaurant(db):
    resto_in = schemas.RestaurantCreate(nom="Chez Test", adresse="Rue A")
    resto = crud.create_restaurant(db, resto_in)

    update_data = schemas.RestaurantCreate(
        nom="Chez Test Updated",
        adresse="Rue B",
        localisation=schemas.LocalisationCreate(ville="Lyon"),
        informations=schemas.InformationsCreate(category="Pizza")
    )

    updated = crud.update_restaurant(db, resto.id, update_data)
    assert updated.nom == "Chez Test Updated"
    assert updated.adresse == "Rue B"
    assert updated.localisation.ville == "Lyon"
    assert updated.informations.category == "Pizza"


def test_delete_restaurant(db):
    resto_in = schemas.RestaurantCreate(nom="Chez Delete", adresse="Rue C")
    resto = crud.create_restaurant(db, resto_in)

    success = crud.delete_restaurant(db, resto.id)
    assert success is True

    deleted = crud.read_restaurant(db, resto.id)
    assert deleted is None
