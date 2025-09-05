import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.core.database import Base
from backend.main import app, get_db

# --- Config DB SQLite en mémoire (indépendante de MySQL) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Fixture DB ---
@pytest.fixture(scope="function", autouse=True)
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# --- Override get_db ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- Tests API ---
def test_create_restaurant():
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


def test_read_restaurants():
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
    assert len(data) == 1
    assert data[0]["nom"] == "Chez Test"


def test_update_restaurant():
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
        json={
            "nom": "Chez Update Updated",
            "adresse": "789 rue Z",
            "localisation": {"ville": "Nice"},
            "informations": {"category": "Burger"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Chez Update Updated"
    assert data["localisation"]["ville"] == "Nice"


def test_delete_restaurant():
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
