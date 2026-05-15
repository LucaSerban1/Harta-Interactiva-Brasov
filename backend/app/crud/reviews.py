from sqlalchemy.orm import Session
from sqlalchemy import func
import bleach
from app.models.reviews import Review
from app.models.location import Location

ALLOWED_TAGS = []  # niciun tag HTML permis

def get_by_location(db: Session, location_id: int, limit: int = 10):
    return db.query(Review)\
             .filter(Review.location_id == location_id)\
             .order_by(Review.created_at.desc())\
             .limit(limit).all()

def create(db: Session, location_id: int, user_id: int,
           rating: float, text: str):
    clean_text = bleach.clean(text, tags=ALLOWED_TAGS, strip=True)

    review = Review(
        location_id=location_id,
        user_id=user_id,
        rating=rating,
        text=clean_text
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    avg = db.query(func.avg(Review.rating))\
            .filter(Review.location_id == location_id).scalar()
    db.query(Location)\
      .filter(Location.id == location_id)\
      .update({"rating_avg": round(avg, 2)})
    db.commit()

    return review

def delete(db: Session, review_id: int, user_id: int, is_admin: bool):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return None, "not_found"
    if review.user_id != user_id and not is_admin:
        return None, "forbidden"
    db.delete(review)
    db.commit()
    return review, None