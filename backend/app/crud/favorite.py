from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from app.models.location import Location

def get_favorites(db: Session, user_id: int):
    favorites = db.query(Favorite)\
                  .filter(Favorite.user_id == user_id)\
                  .all()
    location_ids = [f.location_id for f in favorites]
    if not location_ids:
        return []
    return db.query(Location)\
             .filter(Location.id.in_(location_ids))\
             .all()

def add_favorite(db: Session, user_id: int, location_id: int):
    favorite = Favorite(user_id=user_id, location_id=location_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

def remove_favorite(db: Session, user_id: int, location_id: int):
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.location_id == location_id
    ).first()
    if favorite:
        db.delete(favorite)
        db.commit()
    return favorite

def is_favorite(db: Session, user_id: int, location_id: int) -> bool:
    return db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.location_id == location_id
    ).first() is not None

def get_favorite(db: Session, user_id: int, location_id: int):
    return db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.location_id == location_id
    ).first()