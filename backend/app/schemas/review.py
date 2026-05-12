from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewIn(BaseModel):
    location_id: int
    rating: float = Field(ge=1, le=5)        
    text: str = Field(min_length=10, max_length=1000)  

class ReviewOut(BaseModel):
    id: int
    location_id: int
    user_id: int
    rating: float
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}