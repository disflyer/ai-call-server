from sqlalchemy.orm import Session
from app.models.shop import Shop
from app.schemas.shop import ShopCreate, ShopUpdate

# 创建商店
def create_shop(db: Session, shop: ShopCreate) -> Shop:
    db_shop = Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

# 获取商店列表
def get_shops(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Shop).offset(skip).limit(limit).all()

# 获取单个商店
def get_shop(db: Session, shop_id: int):
    return db.query(Shop).filter(Shop.id == shop_id).first()

# 更新商店
def update_shop(db: Session, shop_id: int, shop: ShopUpdate):
    db_shop = get_shop(db, shop_id)
    if not db_shop:
        return None
    for k, v in shop.dict(exclude_unset=True).items():
        setattr(db_shop, k, v)
    db.commit()
    db.refresh(db_shop)
    return db_shop

# 删除商店
def delete_shop(db: Session, shop_id: int):
    db_shop = get_shop(db, shop_id)
    if not db_shop:
        return None
    db.delete(db_shop)
    db.commit()
    return db_shop 