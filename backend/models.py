from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Localisation(Base):
    __tablename__ = "localisations"

    id = Column(Integer, primary_key=True, index=True)
    ville = Column(String, nullable=False)
    code_postal = Column(String, nullable=True)
    pays = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)


class Informations(Base):
    __tablename__ = "informations"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=True)
    note = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    review = Column(String, nullable=True)


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    adresse = Column(String, nullable=True)

    # Clés étrangères vers les tables localisation et informations
    localisation_id = Column(Integer, ForeignKey("localisations.id"))
    informations_id = Column(Integer, ForeignKey("informations.id"))

    # Relations ORM
    localisation = relationship("Localisation")
    informations = relationship("Informations")
