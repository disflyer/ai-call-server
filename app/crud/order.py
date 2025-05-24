from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate

# 新增或更新订单（有id则更新，无id则新增）
def upsert_order(db: Session, order: OrderCreate, user_id: int) -> Order:
    if hasattr(order, 'id') and getattr(order, 'id', None):
        db_order = db.query(Order).filter(Order.id == order.id, Order.user_id == user_id).first()
        if not db_order:
            return None
        for k, v in order.dict(exclude_unset=True).items():
            if k not in ('id', 'user_id'):
                setattr(db_order, k, v)
        db.commit()
        db.refresh(db_order)
        return db_order
    else:
        data = order.dict(exclude={"user_id"})
        db_order = Order(**data, user_id=user_id)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

# 获取订单列表（仅当前用户）
def get_orders(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

# 获取单个订单（仅当前用户）
def get_order(db: Session, order_id: int, user_id: int):
    return db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()

# 删除订单（仅当前用户）
def delete_order(db: Session, order_id: int, user_id: int):
    db_order = get_order(db, order_id, user_id)
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    return db_order 