import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.core.database import Base
from backend.main import app, get_db

# --- Config DB SQLite pour les tests ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # garde la même connexion pour tous les tests
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Fixture DB ---
@pytest.fixture(scope="function")
def db_session():
    # Recrée les tables avant chaque test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Supprime les tables après le test → DB propre
        Base.metadata.drop_all(bind=engine)

# Override get_db avec la fixture
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- Tests API ---

def test_create_restaurant(db_session):
    response = client.post(
        "/restaurants/",
        json={
            "nom": "Chez Adrien",
            "adresse": "123 rue X",
            "localisation": {"ville": "Paris", "code_postal": "75000", "pays": "France"},
            "informations": {"category": "Italien", "note": 5, "description": "Super pasta"}
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Chez Adrien"
    assert data["localisation"]["ville"] == "Paris"
    assert data["informations"]["category"] == "Italien"


def test_read_restaurants(db_session):
    # Crée un resto pour le test
    client.post(
        "/restaurants/",
        json={
            "nom": "Chez Test",
            "adresse": "456 rue Y",
            "localisation": {"ville": "Lyon"},
            "informations": {"category": "Pizza"}
        },
    )
    response = client.get("/restaurants/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["nom"] == "Chez Test"


def test_update_restaurant(db_session):
    # Crée un resto à mettre à jour
    client.post(
        "/restaurants/",
        json={
            "nom": "Chez Update",
            "adresse": "789 rue Z",
            "localisation": {"ville": "Marseille"},
            "informations": {"category": "Burger"}
        },
    )
    response = client.put(
        "/restaurants/1",
        json={"nom": "Chez Update Updated", "localisation": {"ville": "Nice"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Chez Update Updated"
    assert data["localisation"]["ville"] == "Nice"


def test_delete_restaurant(db_session):
    # Crée un resto à supprimer
    client.post(
        "/restaurants/",
        json={
            "nom": "Chez Delete",
            "adresse": "321 rue W",
            "localisation": {"ville": "Toulouse"},
            "informations": {"category": "Sushi"}
        },
    )
    response = client.delete("/restaurants/1")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True

    # Vérifie qu'il n'existe plus
    response = client.get("/restaurants/1")
    assert response.status_code == 404
