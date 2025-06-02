from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.shop import ShopCreate, ShopUpdate, ShopInDB, ShopBase
from app.crud import shop as crud_shop
from app.models.base import SessionLocal
from typing_extensions import TypedDict
from app.core.auth import get_current_user
from app.models.user import User
from google import genai
import os
import logging
from pydantic import BaseModel
import re
from app.crud.shop import get_shop_by_name_and_address
import json
import requests

router = APIRouter(prefix="/shops", tags=["shops"])

# 配置日志
logger = logging.getLogger(__name__)

# Gemini API 配置
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
client = genai.Client(api_key=GEMINI_API_KEY)

# 请求模型
class GoogleMapParseRequest(BaseModel):
    google_map_url: str

class ShopSchema(TypedDict):
    name: str
    rating: float
    phone: str
    address: str
    # image_url: str
    open_hours: str

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

def resolve_redirect(url):
    try:
        resp = requests.get(url, allow_redirects=True, timeout=10)
        return resp.url
    except Exception as e:
        logger.warning(f"重定向失败，使用原始URL: {e}")
        return url

def parse_google_map_with_gemini(google_map_url: str) -> dict:
    """
    使用Gemini AI结构化输出解析Google Map链接，先重定向短链，利用其内置web search能力
    """
    try:
        # 先处理短链重定向
        final_url = resolve_redirect(google_map_url)
        logger.info(f"最终解析URL: {final_url}")

        prompt = f"""
        请访问这个Google Maps链接并提取店铺信息：{final_url}

        请仔细分析该Google Maps页面，提取以下店铺信息：
        1. 店铺完整名称
        2. 店铺评分（1-5分）
        3. 电话号码（包含国际/地区代码）
        4. 完整详细地址
        5. 营业时间信息
        - rating 必须是数字格式（如：4.5, 3.8），找不到设置为 0.0
        """

        model_options = [
            'gemini-2.0-flash-lite',
            'gemini-2.0-flash',
            'gemini-2.5-flash-preview-05-20',
        ]

        response = None
        last_error = None
        for model_name in model_options:
            try:
                logger.info(f"尝试使用模型: {model_name}")
                generation_config = {
                "response_mime_type": "application/json",
                "temperature": 0,
                "response_schema": ShopSchema,
            }
                response = client.models.generate_content(
                    contents=prompt,
                    config=generation_config,
                    model=model_name
                )
                logger.info(f"成功使用模型: {model_name}")
                logger.info(f"模型结构化响应: {response.text}")
                logger.info(f"Gemini原始响应: {getattr(response, 'text', '')}")
                break
            except Exception as model_error:
                logger.warning(f"模型 {model_name} 失败: {model_error}")
                last_error = model_error
                continue
        if response is None:
            raise Exception(f"所有模型都失败了，最后一个错误: {last_error}")

        # 兼容structured_output或text
        shop_data = getattr(response, "structured_output", None) or (response.text and json.loads(response.text)) or {}
        logger.info(f"Gemini结构化输出: {shop_data}")

        # 数据验证和清理
        shop_data = {
            "name": shop_data.get("name", "未知店铺"),
            "rating": float(shop_data.get("rating", 0.0)) if shop_data.get("rating") is not None else 0.0,
            "phone": shop_data.get("phone") if shop_data.get("phone") not in [None, "", "未提供", "null"] else "未提供",
            "address": shop_data.get("address", "地址未知"),
            "image_url": shop_data.get("image_url") if shop_data.get("image_url") not in [None, "", "null"] else None,
            "open_hours": shop_data.get("open_hours") if shop_data.get("open_hours") not in [None, "", "未知", "null"] else None
        }

        # 处理image_url，截取问号前的部分来简化URL，并加强校验
        if shop_data["image_url"]:
            original_url = shop_data["image_url"]
            # 1. 长度校验
            if len(original_url) > 200:
                logger.warning(f"图片URL过长({len(original_url)}字符)，设为None")
                shop_data["image_url"] = None
            # 2. 必须以 https://lh 开头且包含 googleusercontent.com
            elif not original_url.startswith('https://lh') or 'googleusercontent.com' not in original_url:
                logger.warning(f"图片URL格式不正确，设为None: {original_url[:100]}...")
                shop_data["image_url"] = None
            # 3. 必须包含 /p/AF1Qip 结构
            elif '/p/AF1Qip' not in original_url:
                logger.warning(f"图片URL不包含真实图片ID，设为None: {original_url[:100]}...")
                shop_data["image_url"] = None
            # 4. 禁止出现大量 0-0-0-0-0 或 -0-0-0-0-0 片段
            elif re.search(r'(?:0-){4,}|(?:-0){4,}', original_url):
                logger.warning(f"图片URL包含异常重复片段，设为None: {original_url[:100]}...")
                shop_data["image_url"] = None
            # 5. 截取问号前的部分
            elif '?' in original_url:
                clean_url = original_url.split('?')[0]
                shop_data["image_url"] = clean_url
                logger.info(f"简化图片URL: {original_url[:50]}... -> {clean_url}")
            else:
                logger.info(f"图片URL格式正确: {original_url}")

        logger.info(f"最终解析结果: {shop_data}")
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

        # 调试：结构化输出为空时打印Gemini原始响应
        if not any([shop_data.get("name"), shop_data.get("address"), shop_data.get("phone")]):
            logger.warning(f"Gemini结构化输出为空，建议检查prompt或模型能力。")

        # 查重：同名同址同用户只保留一条
        exist_shop = get_shop_by_name_and_address(db, shop_data["name"], shop_data["address"], user_id=current_user.id)
        if exist_shop:
            logger.info(f"已存在同名同址店铺，直接返回: {exist_shop.name}")
            return exist_shop
        
        # 创建ShopCreate对象，补充user_id
        shop_create = ShopCreate(
            name=shop_data["name"],
            rating=shop_data["rating"],
            phone=shop_data["phone"],
            address=shop_data["address"],
            image_url=shop_data["image_url"],
            open_hours=shop_data["open_hours"],
            user_id=current_user.id
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