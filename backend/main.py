from fastapi import FastAPI, HTTPException
from models import Restaurant
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
    inserted_id = crud.add_restaurant(resto)
    return {"message": "Restaurant ajouté", "id": inserted_id}

@app.put("/restaurants/{resto_id}")
def update_restaurant_note(resto_id: int, note: int):
    affected = crud.update_restaurant(resto_id, note)
    if affected == 0:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return {"message": "Note mise à jour"}

@app.delete("/restaurants/{resto_id}")
def delete_restaurant(resto_id: int):
    affected = crud.delete_restaurant(resto_id)
    if affected == 0:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return {"message": "Restaurant supprimé"}
