from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.order import OrderStatus

class OrderBase(BaseModel):
    customer_name: str
    party_size: int
    phone: str
    arrive_time: datetime
    remark: Optional[str] = None
    shop_id: int
    status: OrderStatus = OrderStatus.created
    user_id: Optional[int] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    id: int

class OrderInDB(OrderBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True 