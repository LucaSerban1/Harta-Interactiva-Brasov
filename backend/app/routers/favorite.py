from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.location import Location
from app.crud import favorite as crud_favorites

router = APIRouter()
security = HTTPBearer()

@router.get("/")
def get_favorites(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user)
):
    return crud_favorites.get_favorites(db, current_user.id)

@router.post("/{location_id}")
def add_favorite(
    location_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user)
):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Locația nu există")

    if crud_favorites.is_favorite(db, current_user.id, location_id):
        raise HTTPException(status_code=400, detail="Locație deja la favorite")

    crud_favorites.add_favorite(db, current_user.id, location_id)
    return {"message": "Adăugat la favorite", "location_id": location_id}

@router.delete("/{location_id}")
def remove_favorite(
    location_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user)
):
    favorite = crud_favorites.get_favorite(db, current_user.id, location_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Nu e la favorite")

    crud_favorites.remove_favorite(db, current_user.id, location_id)
    return {"message": "Eliminat din favorite", "location_id": location_id}

@router.get("/check/{location_id}")
def check_favorite(
    location_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user)
):
    return {"is_favorite": crud_favorites.is_favorite(db, current_user.id, location_id)}