from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, nickname=user.nickname)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first() 