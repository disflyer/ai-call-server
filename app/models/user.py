from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # 验证码登录可不存密码
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    nickname = Column(String(50), nullable=True) 