from sqlalchemy.orm import Session
from app.models.shop import Shop
from app.schemas.shop import ShopCreate, ShopUpdate
from sqlalchemy.exc import IntegrityError

# 新增或更新商店（有id则更新，无id则新增）
def upsert_shop(db: Session, shop: ShopCreate, user_id: int) -> Shop:
    if hasattr(shop, 'id') and getattr(shop, 'id', None):
        db_shop = db.query(Shop).filter(Shop.id == shop.id, Shop.user_id == user_id).first()
        if not db_shop:
            return None
        for k, v in shop.dict(exclude_unset=True).items():
            if k not in ('id', 'user_id'):
                setattr(db_shop, k, v)
        try:
            db.commit()
            db.refresh(db_shop)
            return db_shop
        except IntegrityError:
            db.rollback()
            raise ValueError("Google Map URL已存在，无法重复添加")
    else:
        data = shop.dict(exclude={"user_id"})
        db_shop = Shop(**data, user_id=user_id)
        db.add(db_shop)
        try:
            db.commit()
            db.refresh(db_shop)
            return db_shop
        except IntegrityError:
            db.rollback()
            raise ValueError("Google Map URL已存在，无法重复添加")

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

def get_shop_by_name_and_address(db: Session, name: str, address: str, user_id: int):
    """
    根据店铺名、地址和用户ID查找唯一店铺
    """
    return db.query(Shop).filter(Shop.name == name, Shop.address == address, Shop.user_id == user_id).first()

def get_shop_by_google_map_url(db: Session, google_map_url: str):
    """
    根据Google Map URL查找店铺（全局唯一，不限用户）
    """
    return db.query(Shop).filter(Shop.google_map_url == google_map_url).first() 