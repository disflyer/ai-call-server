from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.shop import ShopCreate, ShopUpdate, ShopInDB
from app.crud import shop as crud_shop
from app.models.base import SessionLocal
from typing import List
from app.core.auth import get_current_user
from app.models.user import User
import google.generativeai as genai
import requests
import os
import logging
from pydantic import BaseModel

router = APIRouter(prefix="/shops", tags=["shops"])

# 配置日志
logger = logging.getLogger(__name__)

# Gemini API 配置
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
genai.configure(api_key=GEMINI_API_KEY)

# 请求模型
class GoogleMapParseRequest(BaseModel):
    google_map_url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ShopInDB)
def upsert_shop(shop: ShopCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = crud_shop.upsert_shop(db, shop, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Shop not found or no permission")
    return result

@router.get("/", response_model=List[ShopInDB])
def list_shops(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_shop.get_shops(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{shop_id}", response_model=ShopInDB)
def get_shop(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_shop = crud_shop.get_shop(db, shop_id, user_id=current_user.id)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.delete("/{shop_id}", response_model=ShopInDB)
def delete_shop(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_shop = crud_shop.delete_shop(db, shop_id, user_id=current_user.id)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found or no permission")
    return db_shop

# 新增：通过Gemini解析Google Map链接的函数
def parse_google_map_with_gemini(google_map_url: str) -> dict:
    """
    使用Gemini AI解析Google Map链接，提取店铺信息
    """
    try:
        # 首先获取Google Map页面内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(google_map_url, headers=headers, timeout=10)
        response.raise_for_status()
        page_content = response.text
        
        # 构建Gemini提示词
        prompt = f"""
        请解析以下Google Map页面内容，提取店铺信息并返回标准JSON格式。
        
        要求返回的JSON格式如下：
        {{
            "name": "店铺名称",
            "rating": 4.5,
            "phone": "电话号码",
            "address": "详细地址",
            "image_url": "店铺图片URL（如果有）",
            "open_hours": "营业时间（如果有）"
        }}
        
        注意事项：
        1. 如果某些信息无法获取，请设置为合理的默认值或null
        2. rating应为浮点数，如果没有评分则设为0.0
        3. phone如果没有则设为"未提供"
        4. 只返回JSON格式，不要其他文字说明
        
        页面内容：
        {page_content[:8000]}  # 限制内容长度避免超出token限制
        """
        
        # 调用Gemini API - 尝试多个可用的模型
        model_options = [
            'gemini-2.0-flash-lite',      # 最快、最具成本效益的模型
            'gemini-2.0-flash',           # 官方文档推荐的主要模型
            'gemini-2.5-flash',           # 最新的多模态模型，具有新一代功能
            'gemini-1.5-flash',           # 稳定的模型作为备选
            'gemini-1.5-flash-latest',    # 最新版本的1.5 Flash
            'gemini-1.5-flash-001'        # 特定版本作为最后备选
        ]
        
        response = None
        last_error = None
        
        for model_name in model_options:
            try:
                logger.info(f"尝试使用模型: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                logger.info(f"成功使用模型: {model_name}")
                break
            except Exception as model_error:
                logger.warning(f"模型 {model_name} 失败: {model_error}")
                last_error = model_error
                continue
        
        if response is None:
            raise Exception(f"所有模型都失败了，最后一个错误: {last_error}")
        
        # 解析Gemini返回的JSON
        import json
        result_text = response.text.strip()
        
        # 尝试提取JSON部分
        if "```json" in result_text:
            json_start = result_text.find("```json") + 7
            json_end = result_text.find("```", json_start)
            result_text = result_text[json_start:json_end].strip()
        elif "```" in result_text:
            json_start = result_text.find("```") + 3
            json_end = result_text.find("```", json_start)
            result_text = result_text[json_start:json_end].strip()
        
        parsed_data = json.loads(result_text)
        
        # 数据验证和清理
        shop_data = {
            "name": parsed_data.get("name", "未知店铺"),
            "rating": float(parsed_data.get("rating", 0.0)),
            "phone": parsed_data.get("phone", "未提供"),
            "address": parsed_data.get("address", "地址未知"),
            "image_url": parsed_data.get("image_url"),
            "open_hours": parsed_data.get("open_hours")
        }
        
        return shop_data
        
    except Exception as e:
        logger.error(f"解析Google Map失败: {e}")
        raise HTTPException(status_code=500, detail=f"解析Google Map失败: {str(e)}")

@router.post("/parse-google-map", response_model=ShopInDB)
def parse_and_create_shop_from_google_map(
    request: GoogleMapParseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    解析Google Map链接，提取店铺信息并保存到数据库
    """
    try:
        # 使用Gemini解析Google Map
        shop_data = parse_google_map_with_gemini(request.google_map_url)
        
        # 创建ShopCreate对象
        shop_create = ShopCreate(
            name=shop_data["name"],
            rating=shop_data["rating"],
            phone=shop_data["phone"],
            address=shop_data["address"],
            image_url=shop_data["image_url"],
            open_hours=shop_data["open_hours"]
        )
        
        # 保存到数据库
        result = crud_shop.upsert_shop(db, shop_create, user_id=current_user.id)
        if not result:
            raise HTTPException(status_code=400, detail="保存店铺信息失败")
            
        logger.info(f"成功解析并保存Google Map店铺: {shop_data['name']}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理Google Map解析请求失败: {e}")
        raise HTTPException(status_code=500, detail=f"处理请求失败: {str(e)}") 