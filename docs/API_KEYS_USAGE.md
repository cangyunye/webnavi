# API Key 使用说明

## 概述

系统现在支持使用 API Key 进行节点管理接口的认证，同时也保留了原有的 JWT Token 认证方式。

## 1. 数据库迁移

首先需要在数据库中创建新的表，使用提供的 SQL 迁移脚本：

```bash
mysql -u your_user -p your_database < sql/api_keys_migration.sql
```

或者使用 Python 自动创建（确保项目配置了正确的数据库连接）：

```python
# 在 Python shell 中运行
from database import engine, Base
Base.metadata.create_all(engine)
```

## 2. API Key 管理

### 创建 API Key

首先登录系统，然后使用以下接口创建 API Key：

**请求：**
```http
POST /api/api-keys
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "key_name": "我的测试 Key",
  "scopes": [],
  "expires_at": "2024-12-31T23:59:59Z"
}
```

**响应：**
```json
{
  "id": 1,
  "key_name": "我的测试 Key",
  "key_prefix": "sk_a1b2c3d4",
  "scopes": [],
  "expires_at": "2024-12-31T23:59:59Z",
  "is_active": 1,
  "last_used_at": null,
  "create_time": "2024-05-14T10:00:00Z",
  "update_time": "2024-05-14T10:00:00Z",
  "api_key": "sk_a1b2c3d4_e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
}
```

**重要：** 完整的 API Key 只会在创建时显示一次，请妥善保存！

### 查看所有 API Key

```http
GET /api/api-keys
Authorization: Bearer <your_jwt_token>
```

### 删除 API Key

```http
DELETE /api/api-keys/{key_id}
Authorization: Bearer <your_jwt_token>
```

### 查看 API Key 使用日志

```http
GET /api/api-keys/{key_id}/logs
Authorization: Bearer <your_jwt_token>
```

## 3. 使用 API Key 调用节点管理接口

### 获取节点列表

```http
GET /api/v1/nodes?page=1&page_size=100
Authorization: Bearer sk_a1b2c3d4_e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

### 创建节点

```http
POST /api/v1/nodes
Authorization: Bearer sk_a1b2c3d4_e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
Content-Type: application/json

{
  "id": "node-001",
  "name": "测试节点",
  "hostname": "test.example.com",
  "address": "192.168.1.100",
  "port": 22,
  "user": "root",
  "status": "active",
  "groups": ["test"],
  "labels": {},
  "ssh_key": "",
  "ssh_password": "",
  "proxy_jump": ""
}
```

### 获取单个节点

```http
GET /api/v1/nodes/node-001
Authorization: Bearer sk_a1b2c3d4_e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

### 更新节点

```http
PUT /api/v1/nodes/node-001
Authorization: Bearer sk_a1b2c3d4_e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
Content-Type: application/json

{
  "id": "node-001",
  "name": "更新后的节点名称",
  "hostname": "test.example.com",
  "address": "192.168.1.100",
  "port": 22,
  "user": "root",
  "status": "active",
  "groups": ["test"],
  "labels": {},
  "ssh_key": "",
  "ssh_password": "",
  "proxy_jump": ""
}
```

### 删除节点

```http
DELETE /api/v1/nodes/node-001
Authorization: Bearer sk_a1b2c3d4_e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

## 4. 使用示例 (Python)

```python
import requests

API_KEY = "sk_a1b2c3d4_e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
BASE_URL = "http://localhost:8000"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 获取节点列表
response = requests.get(f"{BASE_URL}/api/v1/nodes", headers=headers)
print(response.json())

# 创建节点
node_data = {
    "id": "node-001",
    "name": "我的服务器",
    "hostname": "server.example.com",
    "address": "192.168.1.10",
    "port": 22,
    "user": "root",
    "status": "active",
    "groups": ["web"],
    "labels": {"env": "production"},
    "ssh_key": "",
    "ssh_password": "",
    "proxy_jump": ""
}

response = requests.post(
    f"{BASE_URL}/api/v1/nodes",
    headers=headers,
    json=node_data
)
print(response.json())
```

## 5. 安全注意事项

1. **妥善保管 API Key**：API Key 拥有对节点的完全访问权限
2. **设置过期时间**：建议为 API Key 设置合理的过期时间
3. **定期轮换**：定期更换 API Key 以降低风险
4. **监控使用**：定期查看 API Key 的使用日志
5. **立即撤销**：如发现异常使用，立即删除相关 API Key
6. **不要提交到代码库**：绝对不要将 API Key 提交到 Git 或其他代码仓库

## 6. 功能特性

- API Key 使用 bcrypt 加密存储，数据库中仅保存哈希值
- 支持设置过期时间
- 自动记录最后使用时间
- 完整的访问日志记录（IP、User-Agent、时间戳等）
- 支持多个 API Key 并存
- 用户只能查看和管理自己创建的 API Key
