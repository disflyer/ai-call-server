from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate

# 创建订单
def create_order(db: Session, order: OrderCreate) -> Order:
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# 获取订单列表
def get_orders(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Order).offset(skip).limit(limit).all()

# 获取单个订单
def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

# 更新订单
def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    for k, v in order.dict(exclude_unset=True).items():
        setattr(db_order, k, v)
    db.commit()
    db.refresh(db_order)
    return db_order

# 删除订单
def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    return db_order 