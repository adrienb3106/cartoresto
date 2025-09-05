from sqlalchemy.orm import Session
from backend import models, schemas


# CREATE
def create_restaurant(db: Session, resto: schemas.RestaurantCreate) -> models.Restaurant:
    db_localisation = None
    db_informations = None

    if resto.localisation:
        db_localisation = models.Localisation(**resto.localisation.model_dump())
        db.add(db_localisation)
        db.commit()
        db.refresh(db_localisation)

    if resto.informations:
        db_informations = models.Informations(**resto.informations.model_dump())
        db.add(db_informations)
        db.commit()
        db.refresh(db_informations)

    db_resto = models.Restaurant(
        nom=resto.nom,
        adresse=resto.adresse,
        localisation_id=db_localisation.id if db_localisation else None,
        informations_id=db_informations.id if db_informations else None
    )
    db.add(db_resto)
    db.commit()
    db.refresh(db_resto)
    return db_resto


# READ ALL
def read_restaurants(db: Session, skip: int = 0, limit: int = 100) -> list[models.Restaurant]:
    return db.query(models.Restaurant).offset(skip).limit(limit).all()


# READ ONE
def read_restaurant(db: Session, resto_id: int) -> models.Restaurant | None:
    return db.query(models.Restaurant).filter(models.Restaurant.id == resto_id).first()


# UPDATE
def update_restaurant(db: Session, resto_id: int, resto: schemas.RestaurantCreate) -> models.Restaurant | None:
    db_resto = db.query(models.Restaurant).filter(models.Restaurant.id == resto_id).first()
    if not db_resto:
        return None

    db_resto.nom = resto.nom
    db_resto.adresse = resto.adresse

    if resto.localisation:
        if db_resto.localisation:
            for key, value in resto.localisation.model_dump().items():
                setattr(db_resto.localisation, key, value)
        else:
            db_localisation = models.Localisation(**resto.localisation.model_dump())
            db.add(db_localisation)
            db.commit()
            db.refresh(db_localisation)
            db_resto.localisation_id = db_localisation.id

    if resto.informations:
        if db_resto.informations:
            for key, value in resto.informations.model_dump().items():
                setattr(db_resto.informations, key, value)
        else:
            db_informations = models.Informations(**resto.informations.model_dump())
            db.add(db_informations)
            db.commit()
            db.refresh(db_informations)
            db_resto.informations_id = db_informations.id

    db.commit()
    db.refresh(db_resto)
    return db_resto


# DELETE
def delete_restaurant(db: Session, resto_id: int) -> bool:
    db_resto = db.query(models.Restaurant).filter(models.Restaurant.id == resto_id).first()
    if not db_resto:
        return False

    db.delete(db_resto)
    db.commit()
    return True
