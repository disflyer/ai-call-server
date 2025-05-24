from pydantic import BaseModel, Field
from typing import Optional

class ShopBase(BaseModel):
    name: str = Field(..., example="麦当劳")
    rating: Optional[float] = Field(0.0, example=4.5)
    phone: str = Field(..., example="12345678900")
    address: str = Field(..., example="北京市朝阳区xxx路")
    image_url: Optional[str] = Field(None, example="http://img.com/1.jpg")
    open_hours: Optional[str] = Field(None, example="10:00-22:00")

class ShopCreate(ShopBase):
    user_id: Optional[int] = None

class ShopUpdate(ShopBase):
    id: int
    user_id: Optional[int] = None

class ShopInDB(ShopBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True 