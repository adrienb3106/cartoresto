from pydantic import BaseModel
from typing import Optional

# --- Localisation ---
class LocalisationBase(BaseModel):
    ville: Optional[str] = None
    code_postal: Optional[str] = None
    pays: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class ConfigDict:
        from_attributes = True


class LocalisationCreate(LocalisationBase):
    pass


class LocalisationRead(LocalisationBase):
    id: int


# --- Informations ---
class InformationsBase(BaseModel):
    category: Optional[str] = None
    note: Optional[int] = None
    description: Optional[str] = None
    review: Optional[str] = None

    class ConfigDict:
        from_attributes = True


class InformationsCreate(InformationsBase):
    pass


class InformationsRead(InformationsBase):
    id: int


# --- Restaurant ---
class RestaurantBase(BaseModel):
    nom: str
    adresse: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    localisation: Optional[LocalisationCreate] = None
    informations: Optional[InformationsCreate] = None


class RestaurantRead(RestaurantBase):
    id: int
    localisation: Optional[LocalisationRead] = None
    informations: Optional[InformationsRead] = None

    class ConfigDict:
        from_attributes = True
