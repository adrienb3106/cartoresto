import pytest
from sqlalchemy import text
from backend.core.database import SessionLocal, engine

def test_engine_connection():
    """
    Vérifie que l'engine peut se connecter à la base
    """
    # on essaie d'ouvrir une connexion brute
    conn = engine.connect()
    assert conn.closed == False
    conn.close()

def test_session_connection():
    """
    Vérifie qu'on peut ouvrir une session SQLAlchemy et l'utiliser
    """
    db = SessionLocal()
    result = db.execute(text("SELECT 1")).scalar()
    assert result == 1
    db.close()