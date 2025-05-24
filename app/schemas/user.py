from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    nickname: Optional[str] = None

class UserCreate(UserBase):
    code: str = Field(..., description="验证码")
    password: str = Field(..., min_length=6, description="密码")

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="密码")

class UserInDB(UserBase):
    id: int
    class Config:
        from_attributes = True 