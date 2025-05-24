from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserInDB
from app.crud import user as crud_user
from app.models.base import SessionLocal
from typing import List
from fastapi import status
from fastapi.responses import JSONResponse
import random
import string

router = APIRouter(prefix="/users", tags=["users"])

# 简单内存验证码存储
verify_codes = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send_code")
def send_code(email: str):
    code = ''.join(random.choices(string.digits, k=6))
    verify_codes[email] = code
    # 实际项目应通过邮件服务发送验证码
    return {"email": email, "code": code}  # 实际应不返回code

@router.post("/register", response_model=UserInDB)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 测试阶段，验证码随意输入都通过
    # if verify_codes.get(user.email) != user.code:
    #     raise HTTPException(status_code=400, detail="验证码错误")
    db_user = crud_user.create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="用户已存在")
    return db_user

@router.post("/login")
def login(user: UserLogin):
    # 测试阶段，验证码随意输入都通过
    # if verify_codes.get(user.email) != user.code:
    #     raise HTTPException(status_code=400, detail="验证码错误")
    # 实际应返回token
    return {"msg": "登录成功"}

@router.get("/{user_id}", response_model=UserInDB)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user 