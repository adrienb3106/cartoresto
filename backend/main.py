import sys
import os
from dotenv import load_dotenv

# ===== Charger le .env =====
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# ===== Ajouter le backend au PYTHONPATH =====
sys.path.append(os.path.dirname(__file__))

# ===== Import CRUD =====
import crud

# ===== FastAPI =====
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="CartoResto API")

# =========================
# Modèles Pydantic
# =========================
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

# =========================
# Endpoints
# =========================
@app.get("/restaurants")
def list_restaurants():
    return crud.read_restaurants()

@app.get("/restaurants/{resto_id}")
def read_restaurant(resto_id: int):
    resto = crud.get_restaurant(resto_id)
    if not resto:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return resto

@app.post("/restaurants")
def create_restaurant(resto: Restaurant):
    inserted_id = crud.create_restaurant(
        nom=resto.nom,
        adresse=resto.adresse,
        ville=resto.localisation.ville,
        code_postal=resto.localisation.code_postal,
        pays=resto.localisation.pays,
        latitude=resto.localisation.latitude,
        longitude=resto.localisation.longitude,
        category=resto.informations.category,
        note=resto.informations.note,
        description=resto.informations.description,
        review=resto.informations.review
    )
    return {"message": "Restaurant ajouté", "id": inserted_id}

@app.put("/restaurants/{resto_id}")
def update_restaurant(resto_id: int, note: int, pays: Optional[str] = None):
    crud.update_restaurant(restaurant_id=resto_id, note=note)
    if pays:
        crud.update_restaurant_country(restaurant_id=resto_id, country=pays)
    return {"message": "Restaurant mis à jour"}

@app.delete("/restaurants/{resto_id}")
def delete_restaurant(resto_id: int):
    crud.delete_restaurant(restaurant_id=resto_id)
    return {"message": "Restaurant supprimé"}
