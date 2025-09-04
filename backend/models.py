from pydantic import BaseModel

class Restaurant(BaseModel):
    id: int | None = None
    nom: str
    adresse: str
    ville: str
    note: int
    description: str
