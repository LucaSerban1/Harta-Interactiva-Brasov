from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import reviews as crud_reviews
from app.crud import review_reports as crud_reports
from app.schemas.review import ReviewOut, ReviewIn, ReviewReportIn, ReviewReportOut
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/my", response_model=list[ReviewOut])
def get_my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user)
):
    return crud_reviews.get_by_user(db, current_user.id)

@router.get("/reports", response_model=list[ReviewReportOut])
def get_reports(
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Doar adminii pot vedea rapoartele")
    reports = crud_reports.get_all(db)
    result = []
    for r in reports:
        r.review_text = r.review.text if r.review else None
        result.append(r)
    return result

@router.delete("/reports/{report_id}")
def dismiss_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Doar adminii pot gestiona rapoartele")
    if not crud_reports.delete(db, report_id):
        raise HTTPException(status_code=404, detail="Raportul nu există")
    return {"message": "Raport respins"}

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

@router.post("/{review_id}/report", status_code=201)
def report_review(
    review_id: int,
    body: ReviewReportIn,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user)
):
    review = crud_reviews.get_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Recenzia nu există")
    if review.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Nu poți raporta propria recenzie")
    if crud_reports.already_reported(db, review_id, current_user.id):
        raise HTTPException(status_code=409, detail="Ai raportat deja această recenzie")
    crud_reports.create(db, review_id=review_id, reporter_id=current_user.id, reason=body.reason)
    return {"message": "Recenzie raportată"}
