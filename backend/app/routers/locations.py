from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.crud import locations as crud_locations
from app.schemas.location import LocationOut, LocationCreate

router = APIRouter()

@router.get("/", response_model=list[LocationOut])
def get_locations(
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if category or q:
        return crud_locations.search(db, keyword=q, category=category)
    return crud_locations.get_all(db)

@router.get("/{location_id}", response_model=LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = crud_locations.get_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Locația nu există")
    return location

@router.post("/", response_model=LocationOut)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    return crud_locations.create(
        db,
        name=location.name,
        lat=location.lat,
        lng=location.lng,
        category=location.category,
        description=location.description,
        tags=location.tags
    )

@router.patch("/{location_id}")
def update_location(
    location_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    location = crud_locations.get_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Locația nu există")

    for key, value in data.items():
        if hasattr(location, key):
            setattr(location, key, value)

    db.commit()
    db.refresh(location)
    return location

@router.delete("/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    location = crud_locations.get_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Locația nu există")

    db.delete(location)
    db.commit()
    return {"message": "Locație ștearsă"}