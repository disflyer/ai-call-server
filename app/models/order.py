from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class OrderStatus(str, enum.Enum):
    created = "created"
    fail = "fail"
    success = "success"

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    party_size = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
    arrive_time = Column(DateTime, nullable=False)
    remark = Column(Text, nullable=True)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.created, nullable=False)
    shop = relationship('Shop') 