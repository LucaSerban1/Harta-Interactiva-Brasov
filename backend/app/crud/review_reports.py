from sqlalchemy.orm import Session, joinedload
from app.models.review_report import ReviewReport
from app.models.reviews import Review

def create(db: Session, review_id: int, reporter_id: int, reason: str):
    report = ReviewReport(review_id=review_id, reporter_id=reporter_id, reason=reason)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def already_reported(db: Session, review_id: int, reporter_id: int) -> bool:
    return db.query(ReviewReport).filter(
        ReviewReport.review_id == review_id,
        ReviewReport.reporter_id == reporter_id
    ).first() is not None

def get_all(db: Session):
    return db.query(ReviewReport)\
             .options(joinedload(ReviewReport.review), joinedload(ReviewReport.reporter))\
             .order_by(ReviewReport.created_at.desc())\
             .all()

def delete(db: Session, report_id: int):
    report = db.query(ReviewReport).filter(ReviewReport.id == report_id).first()
    if not report:
        return False
    db.delete(report)
    db.commit()
    return True
