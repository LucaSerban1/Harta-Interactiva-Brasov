from pydantic import BaseModel
from typing import Optional

class LocationBase(BaseModel):
    name: str
    lat: float
    lng: float
    category: str
    description: Optional[str] = None
    tags: Optional[list[str]] = []

class LocationCreate(LocationBase):
    pass

class LocationOut(LocationBase):
    id: int
    rating_avg: float
    is_verified: bool

    model_config = {"from_attributes": True}