# 用户权限管理系统实现计划

## 功能概述
实现完整的用户认证和权限管理系统，包含用户注册登录、访客模式、精细权限控制和权限管理后台。

## 功能需求

### 1. 用户认证系统
- **用户注册/登录**：支持邮箱/用户名+密码注册和登录
- **访客模式**：无需注册登录即可访问，但权限受限制
- **会话管理**：使用JWT或Session管理用户认证状态
- **登出功能**

### 2. 权限体系设计
- **访客权限**：
  - 可访问：学习、AI、软件资源、移动通信
  - 不可访问：数据库、研发机器、运维
  - 不能添加/删除资源

- **注册用户权限**：
  - 可访问所有分类
  - 可添加/删除资源（在有访问权限的分类）

- **管理员权限**：
  - 完整访问权限
  - 用户权限管理后台

### 3. 权限管理后台
- 用户列表查看
- 用户角色/权限分配
- 可设置每个用户能访问哪些分类页面

## 数据库设计

### 新增表

#### 1. `users` - 用户表
- `id` - PK
- `username` - 用户名（唯一）
- `email` - 邮箱（唯一）
- `password_hash` - 密码哈希
- `role` - 角色（guest/registered/admin）
- `is_active` - 是否激活
- `create_time`
- `update_time`

#### 2. `user_permissions` - 用户权限表（精细控制）
- `id` - PK
- `user_id` - FK to users
- `category_id` - FK to categories（NULL表示所有分类）
- `permission_type` - 权限类型（view/add/edit/delete）
- `create_time`

#### 3. `roles` - 角色表（可选扩展）
- `id` - PK
- `name` - 角色名
- `description`
- `default_permissions` - JSON格式的默认权限

## 文件变更列表

### 后端
- `sql/init.sql` - 新增用户和权限表，插入默认用户
- `backend/requirements.txt` - 添加密码哈希、JWT等依赖
- `backend/config.py` - 添加认证配置
- `backend/models.py` - 新增User、UserPermission模型
- `backend/schemas.py` - 新增用户认证相关schemas
- `backend/routers/auth.py` - 新文件：认证路由
- `backend/routers/users.py` - 新文件：用户管理路由
- `backend/routers/permissions.py` - 新文件：权限管理路由
- `backend/deps.py` - 新文件：依赖注入（当前用户获取）
- `backend/main.py` - 引入新路由
- `backend/routers/resources.py` - 添加权限检查

### 前端
- `frontend/index.html` - 添加登录/注册页面区域
- `frontend/css/style.css` - 添加认证和管理后台样式
- `frontend/js/app.js` - 添加认证状态、权限控制、管理后台功能

## 实现步骤

### Phase 1: 数据库和基础认证
1. 更新 `sql/init.sql` 新增用户和权限表
2. 安装依赖：`passlib[bcrypt]`, `python-jose[cryptography]` 等
3. 创建User和UserPermission模型
4. 创建认证schemas和路由（注册、登录、访客登录）

### Phase 2: 权限检查机制
1. 在 `routers/resources.py` 中添加权限依赖
2. 创建权限验证依赖函数
3. 前端添加认证状态存储
4. 根据权限渲染侧边栏和卡片

### Phase 3: 权限管理后台
1. 创建用户管理路由（获取用户列表、更新权限）
2. 前端添加管理后台页面
3. 权限分配UI

### Phase 4: UI完善
1. 登录/注册弹窗
2. 用户信息显示和登出
3. 无权限时显示提示

## 权限控制逻辑（简化版）

### 后端
- 使用FastAPI的Dependencies获取当前用户
- 检查用户角色和权限记录
- 未通过时返回403 Forbidden

### 前端
- 保存JWT到localStorage
- 根据权限决定渲染哪些侧边栏项
- 访问无权限分类时显示提示页面
