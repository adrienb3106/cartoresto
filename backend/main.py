from fastapi import FastAPI, HTTPException, Body, Query, Request
from fastapi.templating import Jinja2Templates
import sys
import os
sys.path.append(os.path.dirname(__file__))
from models import Restaurant  # <-- on importe les models
import crud
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from geopy.geocoders import Nominatim

app = FastAPI(title="CartoResto API")

# Chemins pour templates et static
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend_web/templates"))
app.mount("/static", StaticFiles(directory="frontend_web/static"), name="static")

# CORS pour dev local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Géocodeur OpenStreetMap
geolocator = Nominatim(user_agent="cartoresto_app")

def geocode_address(adresse, ville, pays):
    full_address = f"{adresse}, {ville}, {pays}"
    location = geolocator.geocode(full_address)
    if location:
        return location.latitude, location.longitude
    return None, None

# Page d'accueil avec liste des restaurants
@app.get("/")
def home(request: Request):
    restaurants = crud.get_restaurants()
    return templates.TemplateResponse("index.html", {"request": request, "restaurants": restaurants})

# Recherche par nom
@app.get("/restaurants/search")
def search_restaurants(name: str = Query(..., description="Nom ou partie du nom du restaurant")):
    all_restaurants = crud.get_restaurants()
    filtered = [r for r in all_restaurants if name.lower() in r.get("nom", "").lower()]
    return filtered

# Liste complète
@app.get("/restaurants")
def list_restaurants():
    return crud.get_restaurants()

# Détails d'un restaurant
@app.get("/restaurants/{resto_id}")
def read_restaurant(resto_id: int):
    resto = crud.get_restaurant(resto_id)
    if not resto:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return resto

# Création d'un restaurant avec géocodage et validation note
@app.post("/restaurants")
def create_restaurant(resto: dict = Body(...)):
    # Géocodage
    lat, lng = geocode_address(
        resto["adresse"],
        resto["localisation"]["ville"],
        resto["localisation"]["pays"]
    )
    if lat is None or lng is None:
        raise HTTPException(status_code=400, detail="Adresse invalide, impossible de géocoder")

    resto["localisation"]["latitude"] = lat
    resto["localisation"]["longitude"] = lng

    # Limite note 0-10
    note = resto["informations"].get("note", 0)
    note = max(0, min(10, note))
    resto["informations"]["note"] = note

    inserted_id = crud.add_restaurant(
        resto["nom"], resto["adresse"],
        resto["localisation"],
        resto["informations"]
    )
    return {"message": "Restaurant ajouté", "id": inserted_id}

# Page formulaire ajout restaurant
@app.get("/add-restaurant")
def add_restaurant_page(request: Request):
    return templates.TemplateResponse("add_restaurant.html", {"request": request})

# Mise à jour
@app.put("/restaurants/{resto_id}")
def update_restaurant(resto_id: int, fields: dict = Body(...)):
    affected = crud.update_restaurant(resto_id, fields)
    if affected == 0:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return {"message": "Restaurant mis à jour"}

# Suppression
@app.delete("/restaurants/{resto_id}")
def delete_restaurant(resto_id: int):
    affected = crud.delete_restaurant(resto_id)
    if affected == 0:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return {"message": "Restaurant supprimé"}
