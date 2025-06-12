from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from app.models.base import Base
from app.core.config import settings

class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    rating = Column(Float, default=0.0)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=True)
    open_hours = Column(String(100), nullable=True)
    google_map_url = Column(String(500), nullable=True, unique=True, index=True)
    user_id = Column(Integer, ForeignKey(f'{settings.SCHEMA}.users.id'), nullable=False, index=True) 