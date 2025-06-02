# Google Map 解析功能

## 功能描述

新增的Google Map解析功能可以通过Gemini AI智能解析Google Map链接，自动提取店铺信息并保存到数据库中。

## 前置条件

1. **安装依赖**
   ```bash
   poetry install
   # 或
   pip install google-generativeai==0.8.3
   ```

2. **环境变量配置**
   在 `.env` 文件中添加：
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

3. **获取Gemini API Key**
   - 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
   - 创建API Key并配置到环境变量中

## 测试Gemini连接

在配置完成后，运行以下脚本测试Gemini API连接：

```bash
python test_gemini_models.py
```

该脚本会：
- 测试多个Gemini模型版本
- 显示可用的模型列表
- 验证API Key是否正确配置

## API接口

### POST /shops/parse-google-map

解析Google Map链接并创建店铺记录。

**请求参数：**
```json
{
    "google_map_url": "https://maps.app.goo.gl/stMh2zWox4FpZ6kXA"
}
```

**请求头：**
```
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

**响应示例：**
```json
{
    "id": 1,
    "name": "麦当劳(北京王府井店)",
    "rating": 4.2,
    "phone": "010-12345678",
    "address": "北京市东城区王府井大街138号",
    "image_url": "https://maps.gstatic.com/...",
    "open_hours": "06:00-24:00",
    "user_id": 1
}
```

## 解析逻辑

1. **短链重定向处理**：自动跟踪Google Map短链（如 `https://maps.app.goo.gl/xxx`）的重定向，获取最终完整URL
2. **页面内容获取**：使用requests获取重定向后的完整Google Map页面的HTML内容
3. **AI解析**：通过Gemini AI模型解析页面内容，提取结构化的店铺信息
4. **数据验证**：对解析结果进行验证和清理
5. **数据库存储**：将解析后的店铺信息保存到数据库

### 重定向处理详情

Google Map的短链会进行多次重定向才到达最终页面，系统会：

- 自动跟踪所有重定向步骤
- 记录重定向历史和最终URL
- 分析URL参数以获取额外信息
- 使用最终完整URL获取页面内容

这样可以确保获取到最完整、最准确的页面信息，提高解析成功率。

## 支持的信息字段

- `name`: 店铺名称
- `rating`: 评分（0.0-5.0）
- `phone`: 电话号码
- `address`: 详细地址
- `image_url`: 店铺图片URL（可选）
- `open_hours`: 营业时间（可选）

## 测试

运行测试脚本：
```bash
# 通用模型测试
python test_gemini_models.py

# API功能测试
python test_google_map_parser.py

# 特定链接调试测试
python test_google_map_specific.py
```

### 调试Google Map解析问题

如果遇到电话号码或营业时间解析不准确的问题，请按以下步骤调试：

1. **运行专项测试**：
   ```bash
   python test_google_map_specific.py
   ```

2. **检查生成的调试文件**：
   - `debug_google_map_content.html` - 页面原始内容
   - `successful_parse_result.json` - 成功解析的结果

3. **分析页面内容**：
   查看 `debug_google_map_content.html` 文件，搜索以下关键词：
   - 电话号码：`tel:`, `phone`, `电话`, `☎`, `+`
   - 营业时间：`hours`, `营业时间`, `open`, `close`
   - 评分：`rating`, `stars`, `评分`

### 解析准确性优化

当前版本的改进包括：

1. **增强的prompt设计**：
   - 更详细的提取指令
   - 明确的数据格式要求
   - 多种可能的关键词匹配

2. **更好的HTTP请求**：
   - 更完整的请求头
   - 更长的超时时间
   - 更新的User-Agent

3. **改进的JSON解析**：
   - 多种JSON提取策略
   - 错误处理和回退机制
   - 详细的解析日志

4. **优化的模型配置**：
   - 降低temperature提高准确性
   - 合适的token限制
   - 多模型备选机制

## 故障排除

### 常见问题

1. **模型不存在错误**
   ```
   404 models/gemini-pro is not found for API version v1beta
   ```
   
   **解决方案**：
   - 运行 `python test_gemini_models.py` 查看可用模型
   - API已自动尝试多个模型版本，包括最新的 `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-2.0-flash-lite` 等
   - 确保使用最新版本的 `google-generativeai` 包
   
   **最新可用模型**（按优先级排序）：
   - `gemini-2.5-flash`: 最新的多模态模型，具有新一代功能
   - `gemini-2.0-flash`: 官方文档推荐的主要模型
   - `gemini-2.0-flash-lite`: 最快、最具成本效益的模型
   - `gemini-1.5-flash`: 稳定的备选模型

2. **API Key无效**
   ```
   PERMISSION_DENIED: API key not valid
   ```
   
   **解决方案**：
   - 检查 `.env` 文件中的 `GEMINI_API_KEY` 是否正确
   - 确保API Key在Google AI Studio中处于激活状态
   - 验证API Key是否有调用权限

3. **网络连接问题**
   ```
   Connection timeout
   ```
   
   **解决方案**：
   - 检查网络连接
   - 确保能访问 `generativelanguage.googleapis.com`
   - 如在企业网络中，可能需要配置代理

## 注意事项

1. **权限要求**：需要用户登录认证
2. **API限制**：受Gemini API的调用限制
3. **解析准确性**：依赖AI模型的解析能力，可能存在误差
4. **网络要求**：需要能够访问Google Maps和Gemini API
5. **模型兼容性**：系统自动尝试多个模型版本以确保兼容性

## 错误处理

- 无效的Google Map链接
- 网络连接问题
- Gemini API调用失败
- 数据解析错误
- 数据库保存失败

所有错误都会返回相应的HTTP状态码和错误信息。

## 使用示例

```python
import requests

# 登录获取token
login_response = requests.post("http://localhost:8000/users/login", data={
    "username": "your-email@example.com",
    "password": "your-password"
})
token = login_response.json()["access_token"]

# 解析Google Map
response = requests.post(
    "http://localhost:8000/shops/parse-google-map",
    headers={"Authorization": f"Bearer {token}"},
    json={"google_map_url": "https://maps.app.goo.gl/stMh2zWox4FpZ6kXA"}
)

if response.status_code == 200:
    shop_info = response.json()
    print(f"成功创建店铺: {shop_info['name']}")
else:
    print(f"解析失败: {response.text}")
``` 