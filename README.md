# AI Call Server

基于 FastAPI 的智能外呼服务平台，集成 AI 语音通话和店铺信息管理功能。

## 🚀 主要功能

### 1. AI 智能外呼 
- 集成 ElevenLabs 语音 AI，支持自动外呼
- 可定制化 AI Agent 对话内容和首句问候
- 异步任务处理，支持批量外呼
- 实时任务状态跟踪

### 2. 用户管理系统
- 用户注册、登录、验证码发送
- JWT 令牌认证机制
- 安全的密码加密存储

### 3. 订单管理
- 订单增删查改，支持状态跟踪
- 用户级别的数据隔离
- 与 AI 外呼联动

### 4. 店铺管理
- 店铺信息的完整 CRUD 操作
- **🆕 Google Map 智能解析**：通过 Google Gemini 2.5 Flash 自动解析 Google Map 链接，提取店铺信息

## 🆕 Google Map 解析功能

### 功能特色
- **智能解析**：使用 Google Gemini 2.5 Flash 自动提取店铺信息
- **一键导入**：只需提供 Google Map 链接即可创建店铺记录
- **数据完整**：自动提取店铺名称、评分、电话、地址、营业时间等信息
- **格式标准**：返回标准化的 JSON 格式，直接存储到数据库

### 使用方法
```bash
POST /shops/parse-google-map
Content-Type: application/json
Authorization: Bearer <your-token>

{
    "google_map_url": "https://maps.app.goo.gl/stMh2zWox4FpZ6kXA"
}
```

详细使用说明请参考：[Google Map 解析功能文档](./GOOGLE_MAP_PARSER.md)

## 📦 技术栈

- **后端框架**：FastAPI 0.115.12
- **数据库**：PostgreSQL + SQLAlchemy 2.0
- **AI 服务**：
  - ElevenLabs（语音外呼）
  - Google Gemini 2.5 Flash（最新内容解析）
  - Google Gemini 2.0 Flash（高性能内容解析）
- **认证**：JWT + Passlib
- **部署**：Uvicorn + Poetry

## 🛠️ 快速开始

### 1. 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd ai-call-server

# 安装依赖
poetry install
# 或使用 pip
pip install -r requirements.txt
```

### 2. 环境变量配置
创建 `.env` 文件：
```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/ai_call_db

# JWT配置
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ElevenLabs API配置
ELEVENLABS_API_KEY=your-elevenlabs-api-key
ELEVENLABS_AGENT_ID=your-agent-id
ELEVENLABS_PHONE_NUMBER_ID=your-phone-number

# Google Gemini API配置
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. 数据库初始化
```bash
python create_tables.py
```

### 4. 启动服务
```bash
# 开发环境
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生产环境
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 🔗 主要API端点

#### 用户管理
- `POST /users/send-code` - 发送验证码
- `POST /users/register` - 用户注册
- `POST /users/login` - 用户登录
- `GET /users/{user_id}` - 获取用户信息

#### 店铺管理
- `GET /shops/list` - 获取店铺列表
- `POST /shops/upsert` - 创建/更新店铺
- `GET /shops/{shop_id}` - 获取单个店铺
- `DELETE /shops/{shop_id}` - 删除店铺
- `POST /shops/parse-google-map` - 解析Google Map链接

#### 订单管理
- `GET /orders/list` - 获取订单列表
- `POST /orders/upsert` - 创建/更新订单
- `GET /orders/{order_id}` - 获取单个订单
- `DELETE /orders/{order_id}` - 删除订单

#### AI外呼
- `POST /ai-call/start` - 启动AI外呼任务
- `GET /ai-call/status/{task_id}` - 查询任务状态

## 🧪 测试

```bash
# 测试 Google Map 解析功能
python test_google_map_parser.py
```

## 📁 项目结构

```
ai-call-server/
├── app/
│   ├── api/          # API 路由
│   │   ├── ai_call.py    # AI外呼接口
│   │   ├── user.py       # 用户管理
│   │   ├── order.py      # 订单管理
│   │   └── shop.py       # 店铺管理（含Google Map解析）
│   ├── core/         # 核心配置
│   ├── crud/         # 数据库操作
│   ├── models/       # 数据模型
│   └── schemas/      # Pydantic 模式
├── ai_docs/          # 📚 项目文档中心
│   ├── changelogs/   # 变更日志
│   ├── technical/    # 技术文档
│   ├── features/     # 功能文档
│   └── development/  # 开发指南
├── main.py           # 应用入口
├── create_tables.py  # 数据库初始化
└── pyproject.toml    # 依赖配置
```

## 🔧 开发指南

### 代码风格
- 遵循 PEP 8 规范
- 注重代码可读性和复用性
- 适当添加注释说明
- 使用第一性原理思考问题

### 最佳实践
- 精简设计，避免过度工程化
- 使用最新稳定版本的依赖包
- 充分的错误处理和日志记录
- 数据验证和安全检查

## 📚 项目文档

详细的技术文档、变更记录和开发指南请查看：

- **[文档中心](./ai_docs/README.md)** - 完整的项目文档索引
- **[变更日志](./ai_docs/changelogs/)** - 版本更新和功能变更记录
- **[技术文档](./ai_docs/technical/)** - 系统架构和设计文档
- **[功能文档](./ai_docs/features/)** - 各功能模块详细说明

## 📄 许可证

本项目采用 MIT 许可证。