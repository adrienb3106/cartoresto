# backend/tests_backend/TV/conftest.py
import os

# ⚡ Fixer les variables avant tout import
os.environ["DB_USER"] = "dev"
os.environ["DB_PASSWORD"] = "Dev0123456!"
os.environ["DB_HOST"] = "192.168.1.156"
os.environ["DB_PORT"] = "3306"
os.environ["DB_NAME"] = "cartoresto"

print(">>> [TV] Environment DB set to MariaDB on NAS")

import pytest
import backend.models as models
from backend.core import database

@pytest.fixture(scope="session", autouse=True)
def init_real_db():
    # Vérification immédiate
    assert database.DATABASE_URL.startswith("mysql"), f"⚠ Mauvaise DB: {database.DATABASE_URL}"
    print(">>> [TV] Database URL =", database.DATABASE_URL)

    # S’assure que les tables existent
    models.Base.metadata.create_all(bind=database.engine)
    yield
