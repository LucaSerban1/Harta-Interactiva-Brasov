from sqlalchemy.orm import Session
from app.models.location import Location

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