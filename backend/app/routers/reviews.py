from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import reviews as crud_reviews
from app.schemas.review import ReviewOut, ReviewIn

router = APIRouter()

@router.get("/{location_id}", response_model=list[ReviewOut])
def get_reviews(location_id: int, db: Session = Depends(get_db)):
    return crud_reviews.get_by_location(db, location_id)

@router.post("/", response_model=ReviewOut)
def create_review(review: ReviewIn, db: Session = Depends(get_db)):
    return crud_reviews.create(
        db,
        location_id=review.location_id,
        user_id=1,
        rating=review.rating,
        text=review.text
    )