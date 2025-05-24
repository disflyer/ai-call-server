from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.shop import ShopCreate, ShopUpdate, ShopInDB
from app.crud import shop as crud_shop
from app.models.base import SessionLocal
from typing import List

router = APIRouter(prefix="/shops", tags=["shops"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ShopInDB)
def create_shop(shop: ShopCreate, db: Session = Depends(get_db)):
    return crud_shop.create_shop(db, shop)

@router.get("/", response_model=List[ShopInDB])
def list_shops(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud_shop.get_shops(db, skip, limit)

@router.get("/{shop_id}", response_model=ShopInDB)
def get_shop(shop_id: int, db: Session = Depends(get_db)):
    db_shop = crud_shop.get_shop(db, shop_id)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.put("/{shop_id}", response_model=ShopInDB)
def update_shop(shop_id: int, shop: ShopUpdate, db: Session = Depends(get_db)):
    db_shop = crud_shop.update_shop(db, shop_id, shop)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.delete("/{shop_id}", response_model=ShopInDB)
def delete_shop(shop_id: int, db: Session = Depends(get_db)):
    db_shop = crud_shop.delete_shop(db, shop_id)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop 