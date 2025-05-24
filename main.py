from app.main import app

# 创建 FastAPI 实例
app = FastAPI()

# 根路由示例
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}