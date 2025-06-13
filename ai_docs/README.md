# AI Call Server 文档中心

本目录包含AI Call Server项目的所有技术文档、变更记录和开发指南。

## 📁 目录结构

```
ai_docs/
├── README.md                    # 本文件，文档中心说明
├── changelogs/                  # 变更日志
│   ├── api-routes-v1.1.0.md    # API路由优化记录
│   ├── api-routes-v1.1.1.md    # API端点名称优化记录
│   └── google-map-parser-v1.0.0.md # Google Map解析功能开发记录
├── technical/                  # 技术文档
│   ├── database-schema.md      # 数据库设计文档
│   ├── api-design.md          # API设计规范
│   └── deployment.md          # 部署指南
├── features/                   # 功能文档
│   ├── google-map-integration.md  # Google Map集成详细说明
│   ├── ai-calling.md             # AI外呼功能说明
│   └── user-management.md       # 用户管理系统说明
└── development/                # 开发指南
    ├── coding-standards.md    # 编码规范
    ├── testing-guide.md       # 测试指南
    └── contribution.md        # 贡献指南
```

## 📋 文档分类

### 🔄 变更日志 (changelogs/)
记录项目的重要变更、版本更新和功能迭代历史。

### 🔧 技术文档 (technical/)
包含系统架构、数据库设计、API规范等技术相关文档。

### ✨ 功能文档 (features/)
详细描述各个功能模块的设计思路、使用方法和最佳实践。

### 👨‍💻 开发指南 (development/)
为开发者提供编码规范、测试指南和贡献流程。

## 📝 文档编写规范

### 文件命名
- 使用小写字母和连字符
- 包含版本号（如适用）
- 示例：`api-routes-v1.1.0.md`

### 文档结构
每个文档应包含：
1. **标题和版本信息**
2. **变更概述**
3. **详细说明**
4. **技术实现**
5. **测试验证**
6. **影响评估**

### Markdown格式
- 使用标准Markdown语法
- 适当使用emoji增强可读性
- 包含代码示例和配置说明
- 添加必要的图表和流程图

## 🎯 使用指南

### 查找文档
1. **按类型查找**：根据需求选择对应的子目录
2. **按时间查找**：变更日志按时间倒序排列
3. **按功能查找**：功能文档按模块分类

### 贡献文档
1. 在对应目录创建新文档
2. 遵循命名和格式规范
3. 更新本README的目录结构
4. 提交PR进行审核

## 📚 相关资源

- [项目主README](../README.md)
- [Google Map解析功能](../GOOGLE_MAP_PARSER.md)
- [API文档](http://localhost:8000/docs)

---

**维护者**：AI Call Server开发团队  
**最后更新**：2024-12-12 