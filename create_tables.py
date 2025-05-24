from app.models.base import engine, Base
import app.models.shop
import app.models.order
import app.models.user

# 创建所有表
Base.metadata.create_all(bind=engine)
print("所有表已创建")