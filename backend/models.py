from pydantic import BaseModel
from typing import Optional

class Localisation(BaseModel):
    ville: str
    code_postal: str
    pays: str
    latitude: float
    longitude: float

class Informations(BaseModel):
    category: str
    note: int
    description: Optional[str] = None
    review: Optional[str] = None

class Restaurant(BaseModel):
    nom: str
    adresse: str
    localisation: Localisation
    informations: Informations