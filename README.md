# ResourceNav - 资源导航网站

一个基于 Python 3.12 + FastAPI + MySQL 构建的轻量级资源导航系统。

## 功能特性

### 核心功能

- **分类导航**：左侧侧边栏展示所有分类，支持收起/展开
- **主页展示**：卡片式展示分类，点击跳转到对应分类页面
- **资源管理**：支持添加、删除网站资源，支持按分类查看
- **研发环境**：研发机器和数据库实例展示与管理（运维风格）

### 用户系统

- **访客模式**：无需注册登录，可访问部分分类
- **注册登录**：支持用户注册、登录，完整功能访问
- **权限控制**：精细化权限管理
- **管理员后台**：用户管理和权限分配

### 权限体系

系统支持多层级、精细化的权限控制：

#### 角色权限
- **访客**：学习、AI、软件资源、移动通信（仅查看）
- **注册用户**：分类访问、资源编辑
- **管理员**：所有功能 + 用户管理

#### 操作权限
- **可编辑权限**：`can_edit`，允许添加和修改数据
- **可删除权限**：`can_delete`，允许删除数据

#### 分类权限
- 支持为用户设置可访问的分类列表
- 未设置分类权限的注册用户可访问所有分类

#### 覆盖范围
权限控制覆盖：
- 研发机器：查看、添加、修改、删除
- 数据库实例：查看、添加、修改、删除
- 资源：查看、添加、删除
- 用户管理：仅管理员可访问

## 技术栈

### 后端

- **框架**：FastAPI 0.104+
- **数据库**：MySQL 8.0+
- **ORM**：SQLAlchemy 2.0+
- **认证**：JWT (python-jose)
- **密码**：passlib + bcrypt

### 前端

- **HTML5** + **CSS3** + **Vanilla JavaScript**
- **响应式设计**：支持移动端和桌面端

## 快速开始

### 前置要求

- Python 3.12+
- MySQL 8.0+
- Node.js (可选，用于前端开发)

### 安装步骤

#### 1. 克隆项目

```bash
cd d:\webnavi
```

#### 2. 数据库配置

初始化数据库：

```bash
mysql -u root -p < sql/init.sql
```

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`

#### 3. 后端配置

进入后端目录：

```bash
cd backend
```

复制配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 修改数据库连接信息：

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=resource_nav

SECRET_KEY=your_very_secret_key_here_change_in_production
```

安装依赖：

```bash
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
│   │   ├── __init__.py
│   │   ├── auth.py        # 认证路由
│   │   ├── admin.py       # 管理路由
│   │   ├── categories.py  # 分类路由
│   │   └── resources.py   # 资源路由
│   ├── config.py          # 配置管理
│   ├── database.py        # 数据库连接
│   ├── deps.py            # 依赖注入
│   ├── main.py            # FastAPI 应用入口
│   ├── models.py          # SQLAlchemy 模型
│   ├── schemas.py         # Pydantic 模型
│   ├── requirements.txt   # Python 依赖
│   └── .env               # 环境配置
├── frontend/               # 前端代码
│   ├── css/
│   │   └── style.css     # 样式文件
│   ├── js/
│   │   └── app.js        # 前端逻辑
│   └── index.html        # 主页面
├── sql/                   # 数据库脚本
│   └── init.sql          # 初始化脚本
└── docs/                  # 文档目录
```

## API 文档

### 认证相关

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/guest` - 访客登录
- `GET /api/auth/me` - 获取当前用户信息

### 分类相关

- `GET /api/categories` - 获取所有分类

### 资源相关

- `GET /api/resources/{category_id}` - 获取分类资源列表
- `POST /api/resources` - 添加资源
- `DELETE /api/resources/{resource_id}` - 删除资源

### 研发环境

- `GET /api/dev-machines` - 获取研发机器列表
- `GET /api/dev-machines/{machine_id}` - 获取单个研发机器
- `POST /api/dev-machines` - 添加研发机器
- `PUT /api/dev-machines/{machine_id}` - 更新研发机器
- `DELETE /api/dev-machines/{machine_id}` - 删除研发机器

- `GET /api/db-instances` - 获取数据库实例列表
- `GET /api/db-instances/{instance_id}` - 获取单个数据库实例
- `POST /api/db-instances` - 添加数据库实例
- `PUT /api/db-instances/{instance_id}` - 更新数据库实例
- `DELETE /api/db-instances/{instance_id}` - 删除数据库实例

### 管理后台

- `GET /api/admin/users` - 获取用户列表
- `PUT /api/admin/users/{user_id}/role` - 更新用户角色
- `PUT /api/admin/users/{user_id}/status` - 更新用户状态
- `GET /api/admin/users/{user_id}/permissions` - 获取用户权限
- `POST /api/admin/users/{user_id}/permissions` - 添加用户权限
- `DELETE /api/admin/users/{user_id}/permissions/{permission_id}` - 删除用户权限

详细 API 文档请查看 http://localhost:8000/docs

## 数据库设计

### users 表

用户表，存储用户信息。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| username | VARCHAR(50) | 用户名，唯一 |
| email | VARCHAR(100) | 邮箱，唯一 |
| password_hash | VARCHAR(255) | 密码哈希 |
| role | VARCHAR(20) | 角色 (guest/registered/admin) |
| is_active | TINYINT | 是否激活 |
| can_edit | TINYINT | 是否可编辑 |
| can_delete | TINYINT | 是否可删除 |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

### categories 表

分类表。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| name | VARCHAR(50) | 分类名称 |
| icon | VARCHAR(100) | 图标标识 |
| sort_order | INT | 排序 |
| create_time | DATETIME | 创建时间 |

### resources 表

网站资源表。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| category_id | INT | 分类 ID (外键) |
| name | VARCHAR(100) | 资源名称 |
| url | VARCHAR(500) | 资源链接 |
| description | TEXT | 资源描述 |
| status | TINYINT | 状态 |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

### dev_machines 表

研发机器表。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| name | VARCHAR(100) | 机器名称 |
| ip | VARCHAR(50) | IP地址 |
| port | INT | 端口 |
| hostname | VARCHAR(100) | 主机名 |
| cpu | VARCHAR(50) | CPU信息 |
| memory | VARCHAR(50) | 内存信息 |
| disk | VARCHAR(100) | 磁盘信息 |
| os | VARCHAR(100) | 操作系统 |
| status | TINYINT | 状态 (0/1) |
| environment | VARCHAR(50) | 环境 (dev/test/prod) |
| description | TEXT | 描述 |
| create_time | DATETIME | 创建时间 |

### db_instances 表

数据库实例表。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| name | VARCHAR(100) | 实例名称 |
| db_type | VARCHAR(50) | 数据库类型 |
| version | VARCHAR(50) | 版本 |
| ip | VARCHAR(50) | IP地址 |
| port | INT | 端口 |
| charset | VARCHAR(20) | 字符集 |
| status | TINYINT | 状态 (0/1) |
| environment | VARCHAR(50) | 环境 (dev/test/prod) |
| description | TEXT | 描述 |
| create_time | DATETIME | 创建时间 |

### user_permissions 表

用户权限表。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| user_id | INT | 用户 ID (外键) |
| category_id | INT | 分类 ID (外键，可为空) |
| permission_type | VARCHAR(20) | 权限类型 |
| create_time | DATETIME | 创建时间 |

## 默认数据

### 默认分类

1. 学习
2. 数据库
3. 研发机器
4. AI
5. 移动通信
6. 软件资源
7. 运维

### 默认资源

**学习分类**：
- GitHub
- Stack Overflow
- MDN Web Docs
- 菜鸟教程
- LeetCode
- Codecademy

**AI 分类**：
- OpenAI
- Hugging Face
- Stable Diffusion
- MidJourney
- Claude
- Perplexity

**软件资源**：
- VS Code
- Docker
- Notion
- Figma
- Chrome

## 部署指南

### Docker 部署（推荐）

```bash
# 构建镜像
docker build -t resource-nav .

# 运行容器
docker run -p 8000:8000 --env-file .env resource-nav
```

### 生产部署

1. 修改 `.env` 配置，设置强密码和密钥
2. 使用 Gunicorn + Uvicorn 部署
3. 配置 Nginx 反向代理
4. 配置 HTTPS
5. 配置日志轮转

详细部署请查看 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 开发指南

### 后端开发

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端开发

直接编辑 `frontend/` 下的文件，浏览器会自动刷新。

### 数据库迁移

修改模型后需要手动更新数据库或使用迁移工具。

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

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue。
