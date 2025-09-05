from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal, engine
import backend.models as models
import backend.schemas as schemas
import backend.crud as crud
from fastapi.middleware.cors import CORSMiddleware

# Création des tables si elles n'existent pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Autoriser le frontend à parler avec le backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en dev, on autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Dépendance DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Endpoints CRUD ---

@app.post("/restaurants/", response_model=schemas.RestaurantRead)
def create_restaurant(resto: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.create_restaurant(db, resto)


@app.get("/restaurants/", response_model=list[schemas.RestaurantRead])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_restaurants(db, skip=skip, limit=limit)


@app.get("/restaurants/{resto_id}", response_model=schemas.RestaurantRead)
def read_restaurant(resto_id: int, db: Session = Depends(get_db)):
    db_resto = crud.read_restaurant(db, resto_id)
    if db_resto is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_resto


@app.put("/restaurants/{resto_id}", response_model=schemas.RestaurantRead)
def update_restaurant(
    resto_id: int,
    resto: schemas.RestaurantCreate,
    db: Session = Depends(get_db)
):
    db_resto = crud.update_restaurant(db, resto_id, resto)
    if db_resto is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_resto


@app.delete("/restaurants/{resto_id}")
def delete_restaurant(resto_id: int, db: Session = Depends(get_db)):
    success = crud.delete_restaurant(db, resto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"ok": True}
