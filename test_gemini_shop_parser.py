from google import genai
from google.genai import types
import os
import sys
from typing_extensions import TypedDict
import json
import requests

class ShopSchema(TypedDict):
    name: str
    rating: float
    phone: str
    address: str
    image_url: str
    open_hours: str

# 读取API KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
client = genai.Client(api_key=GEMINI_API_KEY)

# 测试用Google Map短链
TEST_URL = sys.argv[1] if len(sys.argv) > 1 else "https://maps.app.goo.gl/stMh2zWox4FpZ6kXA"

# 处理短链重定向，获取最终页面URL
def resolve_redirect(url):
    try:
        resp = requests.get(url, allow_redirects=True, timeout=10)
        return resp.url
    except Exception as e:
        print(f"重定向失败，使用原始URL: {e}")
        return url

FINAL_URL = resolve_redirect(TEST_URL)
print(f"最终解析URL: {FINAL_URL}")

# 测试prompt
PROMPT = f"""
请访问这个Google Maps链接并提取店铺信息：{FINAL_URL}

请仔细分析该Google Maps页面，提取以下店铺信息：
1. 店铺完整名称
2. 店铺评分（1-5分）
3. 电话号码（包含国际/地区代码）
4. 完整详细地址
5. 营业时间信息
6. 店铺主要图片URL
- rating 必须是数字格式（如：4.5, 3.8），找不到设置为 0.0
"""

# 可选模型列表
MODEL_LIST = [
    'gemini-2.0-flash-lite',
    'gemini-2.0-flash',
    'gemini-2.5-flash-preview-05-20',
]

def main():
    for model_name in MODEL_LIST:
        print(f"\n==== 测试模型: {model_name} ====")
        try:
            generation_config = {
                "response_mime_type": "application/json",
                "temperature": 0,
                "response_schema": ShopSchema,
            }
            response = client.models.generate_content(
                contents=PROMPT,
                config=generation_config,
                model=model_name
            )
            print("\n[模型原始响应]:\n", response.text)
            # 兼容structured_output或text
            shop_data = getattr(response, "structured_output", None) or (response.text and json.loads(response.text)) or {}
            print("\n[结构化输出]:\n", shop_data)
        except Exception as e:
            print(f"模型 {model_name} 失败: {e}")

if __name__ == "__main__":
    main() 