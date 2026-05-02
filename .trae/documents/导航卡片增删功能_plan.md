# 导航卡片增删功能实现计划

## 功能概述
为"学习"、"AI"和"软件资源"这三个分类添加：
1. 预填充热门站点卡片
2. 卡片右上角删除按钮
3. 末尾添加卡片（➕）功能

## 当前代码分析
- 已有 `resources` 表和相关模型
- 缺少 Resource 的 schema 和 API
- 前端缺少这三个分类的卡片展示逻辑

## 需要修改的文件

### 后端部分
1. `sql/init.sql` - 添加更多示例资源数据
2. `backend/schemas.py` - 添加 Resource 的 schema
3. `backend/routers/resources.py` - 添加资源的增删查 API

### 前端部分
1. `frontend/js/app.js` - 添加资源卡片渲染、添加、删除逻辑
2. `frontend/css/style.css` - 添加删除按钮和添加卡片样式

## 实现步骤

### 1. 更新数据库初始化脚本 (sql/init.sql)
- 在 `resources` 表中添加更多示例数据
- 学习类：GitHub, Stack Overflow, MDN, 菜鸟教程, LeetCode, Codecademy
- AI类：OpenAI, Hugging Face, Stable Diffusion, MidJourney, Claude, Perplexity
- 软件资源类：VS Code, Docker, Notion, Figma, Chrome

### 2. 更新后端 schemas (backend/schemas.py)
- 添加 `ResourceBase`, `ResourceCreate`, `ResourceResponse` 模型

### 3. 更新后端 routers (backend/routers/resources.py)
- 添加 `GET /api/resources/{category_id}` - 获取分类资源列表
- 添加 `POST /api/resources` - 创建新资源
- 添加 `DELETE /api/resources/{resource_id}` - 删除资源

### 4. 更新前端样式 (frontend/css/style.css)
- 添加卡片右上角删除按钮样式
- 添加添加卡片（➕）样式
- 保持简洁浅色调风格

### 5. 更新前端逻辑 (frontend/js/app.js)
- 修改 `loadCategoryData` 函数
- 为"学习"、"AI"、"软件资源"分类添加卡片渲染逻辑
- 添加删除资源函数
- 添加添加资源对话框逻辑
- 点击链接跳转外部链接

## 热门站点列表

### 学习分类
- GitHub - 代码托管平台
- Stack Overflow - 开发者问答
- MDN Web Docs - Web技术文档
- 菜鸟教程 - 编程教程
- LeetCode - 算法刷题
- Codecademy - 在线学习

### AI分类
- OpenAI - AI 研究公司
- Hugging Face - AI 模型平台
- Stable Diffusion - 图片生成
- MidJourney - AI 绘画
- Claude - Anthropic AI
- Perplexity - AI 搜索

### 软件资源
- VS Code - 代码编辑器
- Docker - 容器平台
- Notion - 笔记工具
- Figma - UI设计
- Chrome - 浏览器

## 卡片设计
- 正常卡片：图标 + 标题 + 描述 + 右上角删除按钮
- 添加卡片：居中➕，边框虚线样式
