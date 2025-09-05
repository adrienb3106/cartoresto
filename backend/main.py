from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal, get_db
from backend import crud, schemas

app = FastAPI(title="Cartoresto API")

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/restaurants/", response_model=schemas.Restaurant)
def create_restaurant(resto: schemas.Restaurant, db: Session = Depends(get_db)):
    return crud.create_restaurant(db, resto)

# READ ALL
@app.get("/restaurants/", response_model=list[schemas.Restaurant])
def read_restaurants(db: Session = Depends(get_db)):
    return crud.get_restaurants(db)

# READ ONE
@app.get("/restaurants/{resto_id}", response_model=schemas.Restaurant)
def read_restaurant(resto_id: int, db: Session = Depends(get_db)):
    resto = crud.get_restaurant(db, resto_id)
    if resto is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return resto

# UPDATE
@app.put("/restaurants/{resto_id}", response_model=schemas.Restaurant)
def update_restaurant(resto_id: int, fields: dict, db: Session = Depends(get_db)):
    resto = crud.update_restaurant(db, resto_id, fields)
    if resto is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return resto

# DELETE
@app.delete("/restaurants/{resto_id}")
def delete_restaurant(resto_id: int, db: Session = Depends(get_db)):
    success = crud.delete_restaurant(db, resto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"ok": True}
