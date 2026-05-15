from sqlalchemy.orm import Session, joinedload
from app.models.location import Location
from app.models.reviews import Review

def get_by_id_with_reviews(db: Session, location_id: int):
    return db.query(Location)\
             .options(joinedload(Location.reviews)\
             .joinedload(Review.user))\
             .filter(Location.id == location_id).first()

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location)\
             .filter(Location.is_verified == True)\
             .offset(skip).limit(limit).all()

def get_by_id(db: Session, location_id: int):
    return db.query(Location)\
             .filter(Location.id == location_id).first()

def search(db: Session, keyword: str = None, category: str = None):
    query = db.query(Location).filter(Location.is_verified == True)

    if category:
        query = query.filter(Location.category == category)

    if keyword:
        query = query.filter(
            Location.name.ilike(f"%{keyword}%") |
            Location.description.ilike(f"%{keyword}%")
        )

    return query.all()

def create(db: Session, name: str, lat: float, lng: float,
           category: str, description: str = None, tags: list = []):
    location = Location(
        name=name, lat=lat, lng=lng,
        category=category, description=description,
        tags=tags, is_verified=True
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

def update(db: Session, location_id: int, data: dict):
    location = get_by_id(db, location_id)
    if not location:
        return None
    for key, value in data.items():
        if hasattr(location, key):
            setattr(location, key, value)
    db.commit()
    db.refresh(location)
    return location

def delete(db: Session, location_id: int):
    location = get_by_id(db, location_id)
    if not location:
        return None
    db.delete(location)
    db.commit()
    return location