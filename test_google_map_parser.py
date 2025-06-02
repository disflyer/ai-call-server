#!/usr/bin/env python3
"""
Google Map 解析功能测试脚本
"""

import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_google_map_parser():
    """
    测试Google Map解析接口
    """
    # API端点
    base_url = "http://localhost:8000"  # 假设服务运行在本地8000端口
    
    # 测试数据
    test_data = {
        "google_map_url": "https://maps.app.goo.gl/stMh2zWox4FpZ6kXA"
    }
    
    # 模拟登录获取token（需要先有用户账号）
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        # 1. 登录获取token
        print("1. 尝试登录...")
        login_response = requests.post(
            f"{base_url}/users/login",
            data=login_data
        )
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("✅ 登录成功")
        else:
            print("❌ 登录失败，请确保有测试用户账号")
            return
        
        # 2. 调用Google Map解析接口
        print("2. 调用Google Map解析接口...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{base_url}/shops/parse-google-map",
            headers=headers,
            json=test_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Google Map解析成功")
            print("解析结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Google Map解析失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("Google Map 解析功能测试")
    print("=" * 50)
    test_google_map_parser() 