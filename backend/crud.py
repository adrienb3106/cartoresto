from sqlalchemy.orm import Session
from backend import models, schemas

# --- CREATE ---
def create_restaurant(db: Session, resto: schemas.Restaurant) -> models.Restaurant:
    """Créer un restaurant avec sa localisation et ses informations"""

    # Créer et persister localisation
    db_localisation = models.Localisation(**resto.localisation.model_dump())
    db.add(db_localisation)
    db.commit()
    db.refresh(db_localisation)

    # Créer et persister informations
    db_informations = models.Informations(**resto.informations.model_dump())
    db.add(db_informations)
    db.commit()
    db.refresh(db_informations)

    # Créer restaurant en liant les deux IDs
    db_restaurant = models.Restaurant(
        nom=resto.nom,
        adresse=resto.adresse,
        localisation_id=db_localisation.id,
        informations_id=db_informations.id
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


# --- READ ---
def get_restaurants(db: Session):
    return db.query(models.Restaurant).all()

def get_restaurant(db: Session, resto_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.id == resto_id).first()


# --- UPDATE ---
def update_restaurant(db: Session, resto_id: int, fields: dict):
    resto = db.query(models.Restaurant).filter(models.Restaurant.id == resto_id).first()
    if not resto:
        return None

    # Mettre à jour Restaurant
    if "nom" in fields:
        resto.nom = fields["nom"]
    if "adresse" in fields:
        resto.adresse = fields["adresse"]

    # Mettre à jour Localisation
    if "localisation" in fields:
        for k, v in fields["localisation"].items():
            setattr(resto.localisation, k, v)

    # Mettre à jour Informations
    if "informations" in fields:
        for k, v in fields["informations"].items():
            setattr(resto.informations, k, v)

    db.commit()
    db.refresh(resto)
    return resto


# --- DELETE ---
def delete_restaurant(db: Session, resto_id: int):
    resto = db.query(models.Restaurant).filter(models.Restaurant.id == resto_id).first()
    if not resto:
        return False

    # Supprimer d’abord le restaurant
    db.delete(resto)

    # Supprimer aussi localisation et informations associées
    if resto.localisation:
        db.delete(resto.localisation)
    if resto.informations:
        db.delete(resto.informations)

    db.commit()
    return True
