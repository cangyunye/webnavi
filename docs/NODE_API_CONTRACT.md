# Node API 接口契约

外部工具通过此接口调用获取节点列表信息。

## 1. 获取节点列表

**请求：**

```http
GET /api/v1/nodes HTTP/1.1
Host: cmdb.example.com
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页数量，默认 100 |
| `name` | string | 否 | 按名称过滤 |
| `group` | string | 否 | 按分组过滤 |
| `label` | string | 否 | 按标签过滤 |
| `status` | string | 否 | 按状态过滤 (active/inactive) |

**响应格式：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 100,
    "items": [
      {
        "id": "node-001",
        "name": "web-server-01",
        "hostname": "web01.example.com",
        "address": "192.168.1.10",
        "port": 22,
        "user": "root",
        "status": "active",
        "groups": ["web", "production"],
        "labels": {
          "env": "prod",
          "region": "cn-east-1",
          "os": "ubuntu22"
        },
        "ssh_key": "/path/to/private/key",
        "ssh_password": "",
        "proxy_jump": "",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-12-01T00:00:00Z"
      }
    ]
  }
}
```

## 2. 获取单个节点

**请求：**

```http
GET /api/v1/nodes/{node_id} HTTP/1.1
Host: cmdb.example.com
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

**响应格式：**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "node-001",
    "name": "web-server-01",
    "hostname": "web01.example.com",
    "address": "192.168.1.10",
    "port": 22,
    "user": "root",
    "status": "active",
    "groups": ["web", "production"],
    "labels": {
      "env": "prod",
      "region": "cn-east-1"
    },
    "ssh_key": "/path/to/private/key",
    "ssh_password": "",
    "proxy_jump": "bastion.example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-12-01T00:00:00Z"
  }
}
```

## 实现参考

项目内实现在 `backend/routers/nodes.py`，认证使用 JWT 或 API Key（见 `docs/API_KEYS_USAGE.md`）。
