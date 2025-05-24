from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    nickname: Optional[str] = None

class UserCreate(UserBase):
    code: str = Field(..., description="验证码")

class UserLogin(BaseModel):
    email: EmailStr
    code: str

class UserInDB(UserBase):
    id: int
    class Config:
        from_attributes = True 