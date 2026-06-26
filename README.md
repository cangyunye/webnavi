# ResourceNav - 资源导航网站

一个基于 Python 3.11+ + FastAPI + MySQL 构建的轻量级资源导航系统，兼具 CMDB 节点管理和运维环境管理能力。

## 功能特性

### 导航与资源

- **分类导航**：左侧侧边栏展示所有分类，支持收起/展开
- **主页展示**：卡片式展示分类，点击跳转到对应分类页面
- **资源管理**：支持添加、删除网站资源，支持按分类查看
- **8 个分类**：学习、数据库、研发机器、AI、测试、软件资源、运维、工具

### 研发环境管理

- **研发机器**：表格展示服务器列表，支持按环境/状态筛选，CRUD 操作
- **数据库实例**：表格展示数据库列表，支持按类型/环境筛选，CRUD 操作
- **组织与责任人**：管理组织和责任人，关联研发机器和数据库

### CMDB 节点管理

- **节点 CRUD**：`/api/v1/nodes`，支持名称/分组/标签/状态过滤
- **双认证**：JWT Token 或 API Key
- **API Key**：bcrypt 加密存储，支持过期时间，使用日志追踪

### 用户系统

- **访客模式**：无需注册登录，可访问部分分类
- **注册登录**：支持用户注册、登录，完整功能访问
- **权限控制**：可编辑/可删除/分类白名单
- **管理员后台**：用户管理、权限分配、管理员可创建用户
- **API Key 管理**：所有用户可创建和管理自己的 API Key
- **枚举管理**：动态下拉选项系统（环境类型、数据库类型等）

### 权限体系

#### 角色权限
- **访客**：学习、AI、软件资源、测试、工具（仅查看）
- **注册用户**：全部分类访问、资源编辑
- **管理员**：所有功能 + 管理后台

#### 操作权限
- **可编辑权限**：`can_edit`，允许添加和修改数据
- **可删除权限**：`can_delete`，允许删除数据

#### 分类权限
- 支持为注册用户设置可访问的分类白名单
- 未设置分类权限的注册用户可访问全部分类

## 技术栈

### 后端

- **框架**：FastAPI (`fastapi[standard]`)
- **数据库**：MySQL 8.0+ (PyMySQL)
- **ORM**：SQLAlchemy 2.0+
- **认证**：JWT (python-jose[cryptography]) + API Key (bcrypt)
- **密码**：bcrypt 直接哈希（无需 passlib）

### 前端

- **HTML5** + **CSS3** + **Vanilla JavaScript**
- **响应式设计**：支持移动端和桌面端

## 快速开始

### 前置要求

- Python 3.11+
- MySQL 8.0+

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repo-url>
cd webnavi
```

#### 2. 数据库配置

初始化数据库（自动创建全部表结构和示例数据）：

```bash
mycli -h 127.0.0.1 -uroot -proot123456 -e "SOURCE sql/init.sql"
```

`init.sql` 内部依次执行 `sql/schema.sql`（12 张表）和 `sql/seed.sql`（示例数据）。

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`

#### 3. 后端配置

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 修改数据库连接信息：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root123456
MYSQL_DATABASE=resource_nav

SECRET_KEY=your_very_secret_key_here_change_in_production
```

安装依赖：

```bash
# 推荐（使用 uv）
uv sync

# 或用 pip
pip install -r requirements.txt
```

启动服务：

```bash
python main.py
```

服务将在 http://localhost:8000 启动

#### 4. 访问应用

打开浏览器访问 http://localhost:8000

API 文档：http://localhost:8000/docs

## 项目结构

```
resource-nav/
├── backend/                 # 后端代码
│   ├── routers/            # API 路由
│   │   ├── auth.py        # 认证路由
│   │   ├── admin.py       # 管理路由（用户管理、凭据）
│   │   ├── categories.py  # 分类路由
│   │   ├── resources.py   # 资源/研发机器/数据库路由
│   │   ├── nodes.py       # CMDB 节点管理
│   │   ├── api_keys.py    # API Key 生命周期管理
│   │   └── enum_items.py  # 枚举项管理
│   ├── main.py            # FastAPI 应用入口
│   ├── config.py          # 配置管理（pydantic-settings）
│   ├── database.py        # 数据库连接
│   ├── models.py          # SQLAlchemy 模型
│   ├── schemas.py         # Pydantic 模型
│   ├── deps.py            # 依赖注入（认证/权限）
│   ├── pyproject.toml     # 项目配置
│   ├── requirements.txt   # Python 依赖
│   ├── uv.lock            # uv 锁定文件
│   └── .env.example       # 环境配置模板
├── frontend/               # 前端代码
│   ├── css/
│   │   └── style.css     # 样式文件
│   ├── js/
│   │   └── app.js        # 前端逻辑
│   └── index.html        # 主页面
├── sql/                   # 数据库脚本
│   ├── init.sql          # 初始化脚本
│   ├── api_keys_migration.sql
│   ├── enum_items_migration.sql
│   └── ...
└── docs/                  # 文档目录
    ├── API.md
    ├── FEATURES.md
    └── ...
```

## API 接口

### 认证

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录（form-data） |
| POST | `/api/auth/guest` | 访客登录 |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 分类与资源

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/categories` | 获取所有分类 |
| GET | `/api/resources/{category_id}` | 获取分类资源列表 |
| POST | `/api/resources` | 添加资源 |
| DELETE | `/api/resources/{resource_id}` | 删除资源 |

### 研发环境

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/dev-machines` | 列表/添加研发机器 |
| GET/PUT/DELETE | `/api/dev-machines/{id}` | 详情/更新/删除 |
| GET/POST | `/api/db-instances` | 列表/添加数据库实例 |
| GET/PUT/DELETE | `/api/db-instances/{id}` | 详情/更新/删除 |
| GET | `/api/organizations` | 获取组织列表 |
| GET | `/api/owners` | 获取责任人列表 |

### 管理后台（仅管理员）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/admin/users` | 用户列表/管理员创建用户 |
| GET | `/api/admin/users/{id}` | 用户详情 |
| PUT | `/api/admin/users/{id}/role` | 更新角色 |
| PUT | `/api/admin/users/{id}/status` | 启用/禁用 |
| PUT | `/api/admin/users/{id}/actions` | 更新操作权限 |
| PUT | `/api/admin/users/{id}/categories` | 设置分类权限 |
| POST | `/api/admin/users/{id}/reset-password` | 重置密码 |
| CRUD | `/api/admin/credentials` | 凭据管理 |

### CMDB 节点 / API Key

| 方法 | 路径 | 说明 |
|------|------|------|
| CRUD | `/api/v1/nodes` | 节点管理（需 JWT 或 API Key） |
| CRUD | `/api/api-keys` | API Key 管理 |
| GET | `/api/api-keys/{id}/logs` | API Key 使用日志 |

### 枚举管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/enum-items` | 枚举项列表 |
| GET | `/api/enum-items/types` | 所有枚举类型 |
| GET | `/api/enum-items/{type}/options` | 下拉选项 |
| POST/PUT/DELETE | `/api/enum-items` | 管理员管理枚举项 |

详细 API 文档请查看 http://localhost:8000/docs

## 默认数据

### 默认分类

| 排序 | 名称 | 访客可访问 |
|------|------|-----------|
| 1 | 学习 | ✅ |
| 2 | 数据库 | ❌ |
| 3 | 研发机器 | ❌ |
| 4 | AI | ✅ |
| 5 | 测试 | ✅ |
| 6 | 软件资源 | ✅ |
| 7 | 运维 | ❌ |
| 8 | 工具 | ✅ |

### 默认资源

**学习**：GitHub, Stack Overflow, MDN Web Docs, 菜鸟教程, LeetCode, Codecademy

**AI**：OpenAI, Hugging Face, Stable Diffusion, MidJourney, Claude, Perplexity

**软件资源**：VS Code, Docker, Notion, Figma, Chrome

**工具**：wttr.in, Public APIs, Papers With Code, Hugging Face Datasets, DevDocs

## 开发指南

### 后端开发

```bash
cd backend
uv sync
python main.py   # uvicorn --reload :8000
```

### 前端开发

直接编辑 `frontend/` 下的文件，浏览器会自动刷新（后端热重载也刷新）。

### 数据库迁移

当 models.py 变更时，需要手动编写 SQL 迁移脚本并放入 `sql/` 目录，然后用 `mycli` 执行：

```bash
mycli -h 127.0.0.1 -uroot -proot123456 resource_nav -e "SOURCE sql/your_migration.sql"
```

## 常见问题

### 注册/登录 422 错误

确保：
- 密码长度至少 6 位
- 用户名没有被占用
- 数据库连接正常

### 访客模式无法访问研发环境

这是设计如此，访客没有权限访问敏感信息。

### API 文档无法访问

确保后端服务正在运行，访问 http://localhost:8000/docs
