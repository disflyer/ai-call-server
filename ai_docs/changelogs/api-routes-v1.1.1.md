# API 端点名称优化变更日志

**版本**：v1.1.1  
**发布日期**：2024-12-12  
**变更类型**：破坏性变更  
**影响范围**：店铺和订单管理端点  

## 🎯 变更概述

将`/*/manage`端点重命名为`/*/upsert`，更准确地反映端点的实际功能。`upsert`是数据库术语，表示"如果存在则更新，不存在则插入"，比`manage`更具体和专业。

## 📋 详细变更

### 店铺管理模块 (`/shops`)

| 原端点 | 新端点 | HTTP方法 | 说明 |
|--------|--------|----------|------|
| `/shops/manage` | `/shops/upsert` | POST | 创建/更新店铺，使用更准确的术语 |

### 订单管理模块 (`/orders`)

| 原端点 | 新端点 | HTTP方法 | 说明 |
|--------|--------|----------|------|
| `/orders/manage` | `/orders/upsert` | POST | 创建/更新订单，使用更准确的术语 |

## 🔧 技术实现

### 修改的文件

1. **`app/api/shop.py`**
   ```python
   # 变更前
   @router.post("/manage", response_model=ShopInDB)
   
   # 变更后
   @router.post("/upsert", response_model=ShopInDB)
   ```

2. **`app/api/order.py`**
   ```python
   # 变更前
   @router.post("/manage", response_model=OrderInDB)
   
   # 变更后
   @router.post("/upsert", response_model=OrderInDB)
   ```

3. **`README.md`**
   - 更新API端点列表中的相关描述

### 函数名称保持不变

虽然端点路径发生变化，但函数名称保持为`upsert_shop`和`upsert_order`，因为它们本来就准确反映了功能。

## ✅ 测试验证

### 端点验证

通过OpenAPI文档确认新端点已正确注册：

```bash
curl -s http://localhost:8000/openapi.json | jq '.paths | keys' | grep upsert
```

预期结果：
```json
"/shops/upsert"
"/orders/upsert"
```

### 功能测试

所有CRUD操作保持正常：
- ✅ 创建新店铺/订单
- ✅ 更新现有店铺/订单
- ✅ 数据验证和权限控制
- ✅ 错误处理机制

## 📊 影响评估

### 破坏性变更

⚠️ **重要提醒**：此次变更为破坏性变更，使用旧端点的客户端需要更新。

**影响的客户端代码**：
```javascript
// 需要更新的调用
fetch('/shops/manage', { method: 'POST' })   → fetch('/shops/upsert', { method: 'POST' })
fetch('/orders/manage', { method: 'POST' })  → fetch('/orders/upsert', { method: 'POST' })
```

### 优势分析

1. **术语准确性**：`upsert`是标准的数据库术语，更专业
2. **功能明确性**：明确表达"插入或更新"的语义
3. **开发者友好**：熟悉数据库的开发者更容易理解
4. **API一致性**：与后端函数名称保持一致

## 🔄 完整的API端点列表

### 用户管理
- `POST /users/send-code` - 发送验证码
- `POST /users/register` - 用户注册
- `POST /users/login` - 用户登录
- `GET /users/{user_id}` - 获取用户信息

### 店铺管理
- `GET /shops/list` - 获取店铺列表
- `POST /shops/upsert` - 创建/更新店铺 ⭐ **已更新**
- `GET /shops/{shop_id}` - 获取单个店铺
- `DELETE /shops/{shop_id}` - 删除店铺
- `POST /shops/parse-google-map` - 解析Google Map链接

### 订单管理
- `GET /orders/list` - 获取订单列表
- `POST /orders/upsert` - 创建/更新订单 ⭐ **已更新**
- `GET /orders/{order_id}` - 获取单个订单
- `DELETE /orders/{order_id}` - 删除订单

### AI外呼
- `POST /ai-call/start` - 启动AI外呼任务
- `GET /ai-call/status/{task_id}` - 查询任务状态

## 📚 相关文档更新

1. **`README.md`** - 更新API端点列表
2. **Swagger UI** - 自动更新，访问`/docs`查看
3. **本变更日志** - 记录此次优化

## 🔄 迁移建议

1. **立即更新**：将所有`/*/manage`调用更新为`/*/upsert`
2. **测试验证**：确保更新后的API调用正常工作
3. **文档同步**：更新相关的集成文档和示例代码

---

**变更负责人**：AI Assistant  
**审核状态**：已通过  
**部署状态**：已部署 