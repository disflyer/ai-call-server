from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.core.config import settings
import enum

class OrderStatus(str, enum.Enum):
    created = "created"
    fail = "fail"
    success = "success"

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    party_size = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    arrive_time = Column(DateTime, nullable=False)
    remark = Column(Text, nullable=True)
    shop_id = Column(Integer, ForeignKey(f'{settings.SCHEMA}.shops.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.created, nullable=False)
    user_id = Column(Integer, ForeignKey(f'{settings.SCHEMA}.users.id'), nullable=False, index=True)
    shop = relationship('Shop') 