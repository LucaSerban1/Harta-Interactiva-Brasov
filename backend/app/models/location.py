from sqlalchemy import Column, Integer, String, Float, Boolean, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    category = Column(String(50))
    description = Column(String(1000))
    rating_avg = Column(Float, default=0.0)
    is_verified = Column(Boolean, default=False)
    tags = Column(ARRAY(String), default=[])

    favorited_by = relationship("Favorite", back_populates="location")
    reviews = relationship("Review", back_populates="location")