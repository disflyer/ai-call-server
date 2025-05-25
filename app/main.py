from fastapi import FastAPI
from app.api import shop, order, user, ai_call

app = FastAPI(title="AI Call Server 订餐API", description="AI帮用户打电话订餐API，自动生成Swagger文档。")

# 注册路由
app.include_router(shop.router)
app.include_router(order.router)
app.include_router(user.router)
app.include_router(ai_call.router) 