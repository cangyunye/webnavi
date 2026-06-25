# 版本日志

所有重要的变更都将记录在此文件中。

## [0.3.0] - 2025-06-25

### 新增

#### 角色体系
- ✅ 新增 **学习导师 (learning_mentor)**：管理学习/AI/软件资源/测试/工具
- ✅ 新增 **运维专家 (ops_expert)**：管理运维/数据库/研发机器
- ✅ 注册用户改为只读，不再具备编辑/删除权限
- ✅ `PUT /api/admin/users/{id}/actions` — 设置 can_edit/can_delete
- ✅ 管理后台角色选择器支持 5 种角色
- ✅ 学习导师/运维专家的 can_edit/can_delete 显示"由角色控制"

#### 状态拓展
- ✅ dev_machines.status 和 db_instances.status 从 TINYINT(0/1) 改为 VARCHAR，支持 online/offline/pending/error 四种状态
- ✅ 统计卡片扩展为在线/待处理/故障/离线四色
- ✅ 状态筛选支持全部四种状态
- ✅ 滑出面板状态选择同步扩展

#### 动态筛选与分页
- ✅ 环境和数据库类型筛选从 `enum_items` API 动态获取
- ✅ 客户端分页，默认 15/页，可切换 30/50/100
- ✅ `<` `>` 翻页箭头

#### 前端增强
- ✅ 浅色/深色主题切换（右上角 🌙/☀️）
- ✅ 主题持久化存储到 localStorage，所有页面共享
- ✅ 右上角退出按钮（清除凭证跳转首页）
- ✅ 统一 `go(url)` 导航函数，解决同 URL 无跳转问题
- ✅ 侧边栏导航跨页面跳转修复（作用域 BUG、同页 hash 无响应）

#### 示例数据
- ✅ 测试分类：Postman, Selenium, Jest, JMeter, Swagger
- ✅ 运维分类：Grafana, Prometheus, Jenkins, Ansible, ELK Stack

### 变更

- ✅ 公开分类访客和注册用户均有访问权限
- ✅ 数据库/研发机器页面仅管理员和运维专家可访问
- ✅ admin.html 补充缺失的"运维"侧边栏按钮
- ✅ category.html / devops.html 侧边栏 数据库/研发机器 正确跳转 devops.html

### 技术栈

- ✅ 前端从单页 SPA（app.js）迁移为 5 页面独立 HTML + 共享 api.js
- ✅ CSS 变量驱动主题，`.dark-theme` class 覆盖

---

## [0.2.0] - 2025-05-02

### 新增

#### 研发环境管理增强

- ✅ 研发机器添加功能（右侧滑出面板）
- ✅ 研发机器修改功能
- ✅ 研发机器删除功能
- ✅ 数据库实例添加功能（右侧滑出面板）
- ✅ 数据库实例修改功能
- ✅ 数据库实例删除功能
- ✅ 添加按钮移到表格顶部
- ✅ 修改按钮在操作列

#### 权限系统增强

- ✅ 完整的权限检查覆盖研发机器和数据库页面
- ✅ `can_edit` 权限控制添加和修改操作
- ✅ `can_delete` 权限控制删除操作
- ✅ 用户分类权限检查
- ✅ 注册用户可设置分类访问权限
- ✅ 未设置分类权限的用户默认可访问所有分类
- ✅ 用户响应数据包含分类权限列表

#### 后端 API 增强

- ✅ `PUT /api/dev-machines/{machine_id}` - 更新研发机器
- ✅ `PUT /api/db-instances/{instance_id}` - 更新数据库实例
- ✅ 所有研发/数据库接口统一权限检查

### 修改

#### 前端改进

- ✅ 修改操作按钮从添加改为修改
- ✅ 添加按钮移到表格顶部
- ✅ 右侧滑出表单支持预填充现有数据
- ✅ 更新 `checkCategoryPermission` 函数，支持分类权限检查

#### 后端改进

- ✅ `UserResponse` 包含 `permissions` 字段
- ✅ 添加 `check_category_permission` 权限检查函数
- ✅ 更新登录、注册、获取用户信息接口返回分类权限
- ✅ 研发机器和数据库接口添加分类权限检查

### 技术栈更新

- ✅ bcrypt 5.0+ (不再依赖 passlib)

---

## [0.1.0] - 2025-05-02

### 新增

#### 核心功能

- ✅ 基础资源导航系统框架
- ✅ 左侧侧边栏导航（支持收起/展开）
- ✅ 主页分类卡片展示
- ✅ 分类页面导航切换
- ✅ 分类：学习、数据库、研发机器、AI、移动通信、软件资源、运维

#### 研发环境管理

- ✅ 研发机器列表页面（运维风格）
- ✅ 数据库实例列表页面（运维风格）
- ✅ 支持按环境筛选（开发/测试/生产）
- ✅ 支持按状态筛选（在线/离线）
- ✅ 状态徽章和环境标识
- ✅ 数据库类型筛选（MySQL/PostgreSQL/Redis/MongoDB等）

#### 资源管理

- ✅ 网站资源卡片展示
- ✅ 添加新资源功能
- ✅ 删除资源功能
- ✅ 为学习、AI、软件资源分类预置热门网站

#### 用户认证系统

- ✅ 用户注册功能
- ✅ 用户登录功能
- ✅ 访客模式（无需注册）
- ✅ JWT Token 认证
- ✅ 密码哈希存储 (bcrypt)
- ✅ 用户退出功能

#### 权限控制

- ✅ 三种用户角色：访客、注册用户、管理员
- ✅ 访客权限限制（仅学习、AI、软件资源、移动通信）
- ✅ 注册用户完整权限
- ✅ 管理员用户管理后台
- ✅ 权限检查中间件

#### 管理后台

- ✅ 用户列表查看
- ✅ 修改用户角色
- ✅ 启用/禁用用户
- ✅ 用户权限查看
- ✅ 添加用户权限
- ✅ 删除用户权限

#### 前端界面

- ✅ 浅色简约风格设计
- ✅ 响应式布局（桌面/平板/手机）
- ✅ 卡片式展示
- ✅ 模态框（登录/注册/添加资源）
- ✅ 平滑动画效果
- ✅ 用户信息展示区域

#### 后端 API

- ✅ FastAPI 后端框架
- ✅ RESTful API 设计
- ✅ 完整的 Swagger 文档
- ✅ SQLAlchemy ORM
- ✅ MySQL 数据库集成
- ✅ 统一错误处理

### 文档

- ✅ 项目 README 文档
- ✅ 部署指南 (DEPLOYMENT.md)
- ✅ API 文档 (API.md)
- ✅ 功能特性文档 (FEATURES.md)
- ✅ 版本日志 (CHANGELOG.md)

### 默认数据

- ✅ 预置 7 个分类
- ✅ 预置 12 台研发机器（开发/测试/生产环境）
- ✅ 预置 11 个数据库实例
- ✅ 预置 17 个网站资源（学习/AI/软件资源分类）
- ✅ 预置管理员账号 (admin/admin123)

### 技术栈

#### 后端

- Python 3.12+
- FastAPI 0.104+
- SQLAlchemy 2.0+
- PyMySQL
- Uvicorn (ASGI server)
- python-jose[cryptography] (JWT)
- passlib[bcrypt] (密码哈希)
- pydantic (数据验证)
- python-dotenv (环境配置)

#### 前端

- HTML5
- CSS3
- Vanilla JavaScript (ES6+)
- 响应式设计

#### 数据库

- MySQL 8.0+
- 字符集：utf8mb4_unicode_ci

### 已知问题

- 暂无

---

## 规划中的功能

### 0.2.0 版本规划

- [ ] 分类管理（添加/编辑/删除分类）
- [ ] 资源编辑功能
- [ ] 资源搜索功能
- [ ] 资源标签系统
- [ ] 用户个人中心
- [ ] 修改密码功能
- [ ] 资源收藏功能
- [ ] 资源访问统计
- [ ] 批量导入资源
- [ ] 导出资源列表
- [ ] 更多主题配色
- [ ] 暗黑模式

### 0.3.0 版本规划

- [ ] OAuth2 第三方登录 (GitHub/Google)
- [ ] 团队协作功能
- [ ] 分享链接功能
- [ ] 评论和点赞
- [ ] 资源评分
- [ ] 推荐算法
- [ ] RSS 订阅
- [ ] 浏览器插件
- [ ] 移动端 App
- [ ] WebSocket 实时通知
- [ ] 操作日志记录

---

## 升级说明

### 从 0.1.0 升级

```bash
# 拉取代码
git pull

# 进入后端目录
cd backend

# 安装新依赖
pip install -r requirements.txt

# 备份数据库
mysqldump -u root -p resource_nav > backup_before_upgrade.sql

# 执行数据库迁移（如果有）
# mysql -u root -p resource_nav < migrations/xxx.sql

# 重启服务
sudo systemctl restart resourcenav
```

---

## 贡献者

感谢所有为项目做出贡献的开发者！

## 版权声明

Copyright © 2025 ResourceNav Team. All rights reserved.
