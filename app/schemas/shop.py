from pydantic import BaseModel
from typing import Optional

class ShopBase(BaseModel):
    name: str
    rating: Optional[float]
    phone: str
    address: str
    image_url: Optional[str]
    open_hours: Optional[str]
    google_map_url: Optional[str]

class ShopCreate(ShopBase):
    user_id: Optional[int]

class ShopUpdate(ShopBase):
    id: int
    user_id: Optional[int]

class ShopInDB(ShopBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True 