from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReviewerInfo(BaseModel):
    id: int
    username: str
    is_admin: bool

    model_config = {"from_attributes": True}

class ReviewOut(BaseModel):
    id: int
    location_id: int
    user_id: int
    rating: float
    text: str
    created_at: datetime
    user: Optional[ReviewerInfo] = None
    location_name: Optional[str] = None

    model_config = {"from_attributes": True}

class ReviewIn(BaseModel):
    location_id: int
    rating: float = Field(ge=1, le=5)
    text: str = Field(min_length=10, max_length=1000)

class ReviewReportIn(BaseModel):
    reason: str = Field(min_length=5, max_length=500)

class ReviewReportOut(BaseModel):
    id: int
    review_id: int
    reason: str
    created_at: datetime
    reporter: Optional[ReviewerInfo] = None
    review_text: Optional[str] = None

    model_config = {"from_attributes": True}
