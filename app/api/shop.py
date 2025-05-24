from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.shop import ShopCreate, ShopUpdate, ShopInDB
from app.crud import shop as crud_shop
from app.models.base import SessionLocal
from typing import List
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/shops", tags=["shops"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ShopInDB)
def upsert_shop(shop: ShopCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = crud_shop.upsert_shop(db, shop, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Shop not found or no permission")
    return result

@router.get("/", response_model=List[ShopInDB])
def list_shops(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_shop.get_shops(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{shop_id}", response_model=ShopInDB)
def get_shop(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_shop = crud_shop.get_shop(db, shop_id, user_id=current_user.id)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.delete("/{shop_id}", response_model=ShopInDB)
def delete_shop(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_shop = crud_shop.delete_shop(db, shop_id, user_id=current_user.id)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found or no permission")
    return db_shop 