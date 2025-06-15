from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY

# 标准异常响应格式
# {"message": str, "code": int, "data": any}

def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = [err['msg'] for err in exc.errors()]
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "; ".join(messages),
            "data": exc.errors()
        }
    )

def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail if exc.detail else "服务器异常",
                "data": None
            }
        )
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(exc) or "服务器内部错误",
            "data": None
        }
    )