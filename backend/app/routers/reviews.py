from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import reviews as crud_reviews
from app.schemas.review import ReviewOut, ReviewIn
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/{location_id}", response_model=list[ReviewOut])
def get_reviews(location_id: int, db: Session = Depends(get_db)):
    return crud_reviews.get_by_location(db, location_id)

@router.post("/", response_model=ReviewOut)
def create_review(
    review: ReviewIn,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user)
):
    return crud_reviews.create(
        db,
        location_id=review.location_id,
        user_id=current_user.id,
        rating=review.rating,
        text=review.text
    )

@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user)
):
    _, error = crud_reviews.delete(db, review_id, current_user.id, current_user.is_admin)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Recenzia nu există")
    if error == "forbidden":
        raise HTTPException(status_code=403, detail="Nu poți șterge recenzia altcuiva")
    return {"message": "Recenzie ștearsă"}