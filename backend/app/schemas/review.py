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

    model_config = {"from_attributes": True}

class ReviewIn(BaseModel):
    location_id: int
    rating: float = Field(ge=1, le=5)
    text: str = Field(min_length=10, max_length=1000)
