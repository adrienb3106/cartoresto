import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.database import Base
from backend import models

# DB SQLite en mémoire pour les tests
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_restaurant_with_relations(db):
    """Créer un restaurant lié à une localisation et des informations"""
    # Créer localisation et informations séparément
    loc = models.Localisation(ville="Paris", code_postal="75000", pays="France")
    info = models.Informations(category="Italien", note=5, description="Super pasta")

    db.add(loc)
    db.add(info)
    db.commit()
    db.refresh(loc)
    db.refresh(info)

    # Créer un restaurant qui les référence
    resto = models.Restaurant(
        nom="Chez Adrien",
        adresse="123 rue X",
        localisation_id=loc.id,
        informations_id=info.id
    )

    db.add(resto)
    db.commit()
    db.refresh(resto)

    # Vérifications
    assert resto.id is not None
    assert resto.nom == "Chez Adrien"
    assert resto.localisation.ville == "Paris"
    assert resto.informations.category == "Italien"
    assert resto.informations.note == 5
