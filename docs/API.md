# API 文档

ResourceNav API 使用 FastAPI 构建，支持自动生成交互式文档。

## 目录

- [基础信息](#基础信息)
- [认证说明](#认证说明)
- [API 接口](#api-接口)
  - [认证接口](#认证接口)
  - [分类接口](#分类接口)
  - [资源接口](#资源接口)
  - [研发机器接口](#研发机器接口)
  - [数据库实例接口](#数据库实例接口)
  - [管理后台接口](#管理后台接口)
- [错误码](#错误码)

## 基础信息

- **Base URL**: `http://localhost:8000` (开发环境)
- **Content-Type**: `application/json` (除非另有说明)
- **API 文档 (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 认证说明

### JWT 认证

除了注册和登录接口，其他需要认证的接口需要在 HTTP Header 中携带 JWT Token：

```http
Authorization: Bearer <token>
```

### 获取 Token

#### 方式一：用户登录

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=testuser&password=test123
```

#### 方式二：访客登录

```http
POST /api/auth/guest
```

### Token 过期

默认过期时间为 7 天 (10080 分钟)。

## API 接口

### 认证接口

#### 1. 用户注册

**接口**：`POST /api/auth/register`

**说明**：注册新用户

**请求体**：

```json
{
  "username": "testuser",
  "password": "password123",
  "email": "user@example.com"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，唯一 |
| password | string | 是 | 密码，至少6位 |
| email | string | 否 | 邮箱，唯一 |

**响应**：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "role": "registered",
    "is_active": 1,
    "can_edit": false,
    "can_delete": false,
    "permissions": [],
    "create_time": "2025-05-02T10:00:00"
  }
}
```

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 400 | 用户名已存在 或 邮箱已被使用 |
| 422 | 请求参数验证失败 |

#### 2. 用户登录

**接口**：`POST /api/auth/login`

**说明**：用户登录获取 Token

**请求**：Form Data (x-www-form-urlencoded)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**响应**：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "is_active": 1,
    "create_time": "2025-05-02T10:00:00"
  }
}
```

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 401 | 用户名或密码错误 |
| 400 | 用户已被禁用 |

#### 3. 访客登录

**接口**：`POST /api/auth/guest`

**说明**：以访客身份登录

**请求**：不需要请求体

**响应**：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 0,
    "username": "guest",
    "role": "guest",
    "is_active": 1
  }
}
```

#### 4. 获取当前用户信息

**接口**：`GET /api/auth/me`

**说明**：获取当前登录用户信息

**需要认证**：是

**响应**：

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin",
  "is_active": 1,
  "create_time": "2025-05-02T10:00:00"
}
```

### 分类接口

#### 1. 获取所有分类

**接口**：`GET /api/categories`

**说明**：获取所有分类列表

**需要认证**：否

**响应**：

```json
[
  {
    "id": 1,
    "name": "学习",
    "icon": "icon-study",
    "sort_order": 1,
    "create_time": "2025-05-02T10:00:00"
  },
  {
    "id": 2,
    "name": "数据库",
    "icon": "icon-database",
    "sort_order": 2,
    "create_time": "2025-05-02T10:00:00"
  },
  {
    "id": 3,
    "name": "研发机器",
    "icon": "icon-dev-machine",
    "sort_order": 3,
    "create_time": "2025-05-02T10:00:00"
  }
]
```

### 资源接口

#### 1. 获取分类资源列表

**接口**：`GET /api/resources/{category_id}`

**说明**：获取指定分类下的资源列表

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category_id | int | 是 | 分类 ID |

**查询参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | int | 否 | 资源状态 (0/1) |

**需要认证**：是 (访客只能访问特定分类)

**响应**：

```json
[
  {
    "id": 1,
    "category_id": 1,
    "name": "GitHub",
    "url": "https://github.com",
    "description": "全球最大的代码托管平台",
    "status": 1,
    "create_time": "2025-05-02T10:00:00",
    "update_time": "2025-05-02T10:00:00"
  }
]
```

**权限要求**：

- 访客：只能访问 id=1 (学习), 4 (AI), 6 (软件资源), 5 (移动通信)
- 注册用户/管理员：可以访问所有

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 403 | 无权限访问此分类 |

#### 2. 添加资源

**接口**：`POST /api/resources`

**说明**：添加新资源

**需要认证**：是 (访客不可用)

**请求体**：

```json
{
  "category_id": 1,
  "name": "新网站",
  "url": "https://example.com",
  "description": "网站描述",
  "status": 1
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category_id | int | 是 | 分类 ID |
| name | string | 是 | 资源名称 |
| url | string | 是 | 资源链接 |
| description | string | 否 | 描述 |
| status | int | 否 | 状态，默认 1 |

**响应**：

```json
{
  "id": 100,
  "category_id": 1,
  "name": "新网站",
  "url": "https://example.com",
  "description": "网站描述",
  "status": 1,
  "create_time": "2025-05-02T10:00:00",
  "update_time": "2025-05-02T10:00:00"
}
```

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 403 | 访客无权限添加资源 |
| 422 | 请求参数验证失败 |

#### 3. 删除资源

**接口**：`DELETE /api/resources/{resource_id}`

**说明**：删除指定资源

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| resource_id | int | 是 | 资源 ID |

**需要认证**：是 (访客不可用)

**响应**：

```json
{
  "message": "资源删除成功"
}
```

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 403 | 访客无权限删除资源 |
| 404 | 资源不存在 |

### 研发机器接口

#### 1. 获取研发机器列表

**接口**：`GET /api/dev-machines`

**说明**：获取所有研发机器列表

**查询参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| environment | string | 否 | 环境 (dev/test/prod) |
| status | int | 否 | 状态 (0/1) |

**需要认证**：是 (访客不可用)

**响应**：

```json
[
  {
    "id": 1,
    "name": "开发服务器-01",
    "ip": "192.168.1.101",
    "port": 22,
    "hostname": "dev-server-01",
    "cpu": "8核 Intel Xeon",
    "memory": "16GB",
    "disk": "500GB SSD",
    "os": "Ubuntu 22.04 LTS",
    "status": 1,
    "environment": "dev",
    "description": "开发测试环境主服务器",
    "create_time": "2025-05-02T10:00:00"
  }
]
```

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 403 | 访客无权限访问 |

#### 2. 获取单个研发机器

**接口**：`GET /api/dev-machines/{machine_id}`

**说明**：获取指定研发机器详情

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| machine_id | int | 是 | 机器 ID |

**需要认证**：是 (访客不可用)

**响应**：同列表中的单个对象

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 403 | 访客无权限访问 |
| 404 | 机器不存在 |

### 数据库实例接口

#### 1. 获取数据库实例列表

**接口**：`GET /api/db-instances`

**说明**：获取所有数据库实例列表

**查询参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| environment | string | 否 | 环境 (dev/test/prod) |
| db_type | string | 否 | 数据库类型 |
| status | int | 否 | 状态 (0/1) |

**需要认证**：是 (访客不可用)

**响应**：

```json
[
  {
    "id": 1,
    "name": "MySQL-主库-dev",
    "db_type": "MySQL",
    "version": "8.0.35",
    "ip": "192.168.2.101",
    "port": 3306,
    "charset": "utf8mb4",
    "status": 1,
    "environment": "dev",
    "description": "开发环境MySQL主库",
    "create_time": "2025-05-02T10:00:00"
  }
]
```

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 403 | 访客无权限访问 |

#### 2. 获取单个数据库实例

**接口**：`GET /api/db-instances/{instance_id}`

**说明**：获取指定数据库实例详情

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| instance_id | int | 是 | 实例 ID |

**需要认证**：是 (访客不可用)

**响应**：同列表中的单个对象

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 403 | 访客无权限访问 |
| 404 | 实例不存在 |

### 管理后台接口

> 注意：需要管理员角色 (role=admin)

#### 1. 获取用户列表

**接口**：`GET /api/admin/users`

**说明**：获取所有用户列表

**需要认证**：是 (管理员)

**响应**：

```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "is_active": 1,
    "create_time": "2025-05-02T10:00:00"
  }
]
```

#### 2. 获取用户详情

**接口**：`GET /api/admin/users/{user_id}`

**说明**：获取指定用户详情

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |

**需要认证**：是 (管理员)

**响应**：同列表中的单个用户对象

#### 3. 更新用户角色

**接口**：`PUT /api/admin/users/{user_id}/role`

**说明**：更新用户角色

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |

**查询参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| role | string | 是 | 角色 (guest/registered/admin) |

**需要认证**：是 (管理员)

**响应**：

```json
{
  "message": "角色更新成功"
}
```

#### 4. 更新用户状态

**接口**：`PUT /api/admin/users/{user_id}/status`

**说明**：启用或禁用用户

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |

**查询参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| is_active | int | 是 | 状态 (0/1) |

**需要认证**：是 (管理员)

**响应**：

```json
{
  "message": "状态更新成功"
}
```

#### 5. 获取用户权限

**接口**：`GET /api/admin/users/{user_id}/permissions`

**说明**：获取指定用户的权限列表

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |

**需要认证**：是 (管理员)

**响应**：

```json
[
  {
    "id": 1,
    "user_id": 1,
    "category_id": 1,
    "permission_type": "view",
    "create_time": "2025-05-02T10:00:00"
  }
]
```

#### 6. 添加用户权限

**接口**：`POST /api/admin/users/{user_id}/permissions`

**说明**：为用户添加权限

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |

**请求体**：

```json
{
  "category_id": 1,
  "permission_type": "edit"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category_id | int | 否 | 分类 ID，空表示所有分类 |
| permission_type | string | 否 | 权限类型，默认 "view" |

**需要认证**：是 (管理员)

**响应**：

```json
{
  "id": 1,
  "user_id": 1,
  "category_id": 1,
  "permission_type": "edit",
  "create_time": "2025-05-02T10:00:00"
}
```

**错误**：

| HTTP 状态码 | 说明 |
|------------|------|
| 404 | 用户不存在 或 分类不存在 |

#### 7. 删除用户权限

**接口**：`DELETE /api/admin/users/{user_id}/permissions/{permission_id}`

**说明**：删除用户权限

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |
| permission_id | int | 是 | 权限 ID |

**需要认证**：是 (管理员)

**响应**：

```json
{
  "message": "权限删除成功"
}
```

#### 8. 更新用户分类权限

**接口**：`PUT /api/admin/users/{user_id}/categories`

**说明**：批量设置用户可访问的分类权限

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |

**请求体**：

```json
{
  "category_permissions": [
    { "category_id": 2, "enabled": true },
    { "category_id": 3, "enabled": true }
  ]
}
```

**需要认证**：是 (管理员)

**响应**：

```json
{
  "message": "分类权限更新成功"
}
```

#### 9. 更新用户操作权限

**接口**：`PUT /api/admin/users/{user_id}/actions`

**说明**：设置用户的编辑和删除权限

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |

**请求体**：

```json
{
  "can_edit": true,
  "can_delete": false
}
```

**需要认证**：是 (管理员)

**响应**：

```json
{
  "message": "操作权限更新成功"
}
```

#### 10. 重置用户密码

**接口**：`POST /api/admin/users/{user_id}/reset-password`

**说明**：管理员重置用户密码

**路径参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户 ID |

**请求体**：

```json
{
  "password": "newpassword123"
}
```

**需要认证**：是 (管理员)

**响应**：

```json
{
  "message": "密码重置成功"
}
```

## 错误码

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 422 | 请求参数验证失败 |
| 500 | 服务器内部错误 |

### 错误响应格式

```json
{
  "detail": "错误描述"
}
```

或验证错误：

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "密码长度至少为6位",
      "input": "123",
      "ctx": {"min_length": 6}
    }
  ]
}
```
