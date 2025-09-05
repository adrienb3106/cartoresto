from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# URL de connexion (SQLAlchemy a besoin de ce format)
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine = connexion à la base
engine = create_engine(DATABASE_URL, echo=True)  
# echo=True = affiche les requêtes SQL dans la console (pratique en dev)

# Session = objet qu’on utilise dans les routes pour parler à la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = classe mère pour nos futurs modèles ORM
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
