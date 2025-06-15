from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from app.api import shop, order, user, ai_call
from app.core.error_handler import request_validation_exception_handler, global_exception_handler

app = FastAPI(title="AI Call Server 订餐API", description="AI帮用户打电话订餐API，自动生成Swagger文档。")


# 注册全局异常处理器
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, global_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


# 注册路由
app.include_router(shop.router)
app.include_router(order.router)
app.include_router(user.router)
app.include_router(ai_call.router)
