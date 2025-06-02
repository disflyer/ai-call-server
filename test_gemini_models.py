#!/usr/bin/env python3
"""
测试 Gemini API 连接和可用模型
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_gemini_models():
    """
    测试不同的Gemini模型
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your-gemini-api-key-here":
        print("❌ 请在 .env 文件中设置正确的 GEMINI_API_KEY")
        return
    
    # 配置API
    genai.configure(api_key=api_key)
    
    # 测试的模型列表
    models_to_test = [
        'gemini-2.5-flash',           # 最新的多模态模型
        'gemini-2.5-pro',             # 最强大的思考型模型（实验性）
        'gemini-2.0-flash',           # 官方推荐的主要模型
        'gemini-2.0-flash-lite',      # 最快、最具成本效益
        'gemini-1.5-flash',           # 稳定的备选模型
        'gemini-1.5-flash-latest',    # 最新版本的1.5 Flash
        'gemini-1.5-flash-001',       # 特定版本
        'gemini-1.5-pro',             # Pro版本
        'gemini-pro'                  # 旧版本（可能已废弃）
    ]
    
    test_prompt = "请用一句话介绍你自己。"
    
    print("🧪 开始测试 Gemini 模型...")
    print("=" * 60)
    
    working_models = []
    
    for model_name in models_to_test:
        try:
            print(f"🔍 测试模型: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(test_prompt)
            
            if response and response.text:
                print(f"✅ {model_name} - 工作正常")
                print(f"   响应: {response.text[:100]}...")
                working_models.append(model_name)
            else:
                print(f"⚠️  {model_name} - 响应为空")
                
        except Exception as e:
            print(f"❌ {model_name} - 失败: {str(e)[:100]}...")
        
        print("-" * 40)
    
    print(f"\n📋 测试总结:")
    print(f"可用模型数量: {len(working_models)}")
    if working_models:
        print("可用模型:")
        for model in working_models:
            print(f"  ✓ {model}")
        print(f"\n💡 建议在代码中使用: {working_models[0]}")
    else:
        print("❌ 没有找到可用的模型，请检查API密钥或网络连接")

def list_available_models():
    """
    列出所有可用的模型
    """
    try:
        print("\n🔍 正在获取所有可用模型...")
        models = genai.list_models()
        
        print("📋 可用模型列表:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"  • {model.name}")
                print(f"    输入token限制: {getattr(model, 'input_token_limit', '未知')}")
                print(f"    输出token限制: {getattr(model, 'output_token_limit', '未知')}")
                print("-" * 30)
                
    except Exception as e:
        print(f"❌ 获取模型列表失败: {e}")

if __name__ == "__main__":
    print("Gemini API 模型测试工具")
    print("=" * 60)
    
    # 测试模型
    test_gemini_models()
    
    # 列出可用模型
    list_available_models()
    
    print("\n🏁 测试完成！") 