from pydantic import BaseModel

class Localisation(BaseModel):
    ville: str
    code_postal: str | None = None
    pays: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class Informations(BaseModel):
    category: str | None = None
    note: int | None = None
    description: str | None = None
    review: str | None = None

class Restaurant(BaseModel):
    nom: str
    adresse: str | None = None
    localisation: Localisation
    informations: Informations
