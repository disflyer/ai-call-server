from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderUpdate, OrderInDB
from app.crud import order as crud_order
from app.models.base import SessionLocal
from typing import List
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upsert", response_model=OrderInDB)
def upsert_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = crud_order.upsert_order(db, order, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found or no permission")
    return result

@router.get("/list", response_model=List[OrderInDB])
def list_orders(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_order.get_orders(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderInDB)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_order = crud_order.get_order(db, order_id, user_id=current_user.id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", response_model=OrderInDB)
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_order = crud_order.delete_order(db, order_id, user_id=current_user.id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found or no permission")
    return db_order 