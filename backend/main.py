from fastapi import FastAPI, HTTPException, Body
import sys
import os
sys.path.append(os.path.dirname(__file__))
from models import Restaurant  # <-- on importe les models
import crud

app = FastAPI(title="CartoResto API")

@app.get("/restaurants")
def list_restaurants():
    return crud.get_restaurants()

@app.get("/restaurants/{resto_id}")
def read_restaurant(resto_id: int):
    resto = crud.get_restaurant(resto_id)
    if not resto:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return resto

@app.post("/restaurants")
def create_restaurant(resto: Restaurant):
    inserted_id = crud.add_restaurant(
        resto.nom, resto.adresse,
        resto.localisation.model_dump(),
        resto.informations.model_dump()
    )
    return {"message": "Restaurant ajouté", "id": inserted_id}

@app.put("/restaurants/{resto_id}")
def update_restaurant(resto_id: int, fields: dict = Body(...)):
    affected = crud.update_restaurant(resto_id, fields)
    if affected == 0:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return {"message": "Restaurant mis à jour"}

@app.delete("/restaurants/{resto_id}")
def delete_restaurant(resto_id: int):
    affected = crud.delete_restaurant(resto_id)
    if affected == 0:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return {"message": "Restaurant supprimé"}
