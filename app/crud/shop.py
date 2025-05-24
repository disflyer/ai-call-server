from sqlalchemy.orm import Session
from app.models.shop import Shop
from app.schemas.shop import ShopCreate, ShopUpdate

# 新增或更新商店（有id则更新，无id则新增）
def upsert_shop(db: Session, shop: ShopCreate, user_id: int) -> Shop:
    if hasattr(shop, 'id') and getattr(shop, 'id', None):
        db_shop = db.query(Shop).filter(Shop.id == shop.id, Shop.user_id == user_id).first()
        if not db_shop:
            return None
        for k, v in shop.dict(exclude_unset=True).items():
            if k not in ('id', 'user_id'):
                setattr(db_shop, k, v)
        db.commit()
        db.refresh(db_shop)
        return db_shop
    else:
        data = shop.dict(exclude={"user_id"})
        db_shop = Shop(**data, user_id=user_id)
        db.add(db_shop)
        db.commit()
        db.refresh(db_shop)
        return db_shop

# 获取商店列表（仅当前用户）
def get_shops(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    return db.query(Shop).filter(Shop.user_id == user_id).offset(skip).limit(limit).all()

# 获取单个商店（仅当前用户）
def get_shop(db: Session, shop_id: int, user_id: int):
    return db.query(Shop).filter(Shop.id == shop_id, Shop.user_id == user_id).first()

# 删除商店（仅当前用户）
def delete_shop(db: Session, shop_id: int, user_id: int):
    db_shop = get_shop(db, shop_id, user_id)
    if not db_shop:
        return None
    db.delete(db_shop)
    db.commit()
    return db_shop 