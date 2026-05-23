有一个外部工具，需要调用API获取节点列表信息，并提供了 接口规范
## API 接口规范

### 1. 获取节点列表

**请求：**

```http
GET /api/v1/nodes HTTP/1.1
Host: cmdb.example.com
Authorization: Bearer {OWL_API_TOKEN}
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

### 2. 获取单个节点

**请求：**

```http
GET /api/v1/nodes/{node_id} HTTP/1.1
Host: cmdb.example.com
Authorization: Bearer {OWL_API_KEY}
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

服务端可以参考以下实现：
- 你不需要完全参考它的实现，主要根据接口规范来
- 在当前项目的前提下，你要提供一个实现，用于获取节点列表和单个节点信息
- 提出当前项目是否需要作出什么更改，或者协议哪些地方当前项目无法提供，可以采取默认值

### Python FastAPI 示例（推荐）

```python
# cmdb_server.py
# 安装依赖: pip install fastapi uvicorn pydantic

from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import os

app = FastAPI(title="CMDB API", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class Node(BaseModel):
    id: str
    name: str
    hostname: Optional[str] = ""
    address: str
    port: int = 22
    user: str = "root"
    status: str = "active"
    groups: List[str] = []
    labels: Dict[str, str] = {}
    ssh_key: Optional[str] = ""
    ssh_password: Optional[str] = ""
    proxy_jump: Optional[str] = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class APIResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None

class NodeListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Node]

# 模拟数据库
NODES_DB: Dict[str, Node] = {}

# 初始化测试数据
def init_test_data():
    global NODES_DB
    NODES_DB = {
        "node-001": Node(
            id="node-001",
            name="web-server-01",
            hostname="web01.example.com",
            address="192.168.1.10",
            port=22,
            user="root",
            status="active",
            groups=["web", "production"],
            labels={"env": "prod", "region": "cn-east-1"},
            ssh_key="/ssh/keys/web01.pem",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        "node-002": Node(
            id="node-002",
            name="db-server-01",
            hostname="db01.example.com",
            address="192.168.1.20",
            port=22,
            user="ubuntu",
            status="active",
            groups=["database", "production"],
            labels={"env": "prod", "region": "cn-east-1"},
            ssh_key="/ssh/keys/db01.pem",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
    }

init_test_data()

# 认证依赖
API_KEY = os.getenv("API_KEY", "sk-secret-key")

async def verify_api_key(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="缺少认证信息")
    token = authorization.replace("Bearer ", "")
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="认证失败")
    return token

# API 路由
@app.get("/api/v1/nodes", response_model=APIResponse)
async def list_nodes(
    name: Optional[str] = Query(None, description="按名称过滤"),
    group: Optional[str] = Query(None, description="按分组过滤"),
    label: Optional[str] = Query(None, description="按标签过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=1000, description="每页数量"),
    authorization: str = Header(None)
):
    await verify_api_key(authorization)

    items = list(NODES_DB.values())

    # 过滤
    if name:
        items = [n for n in items if name.lower() in n.name.lower()]
    if group:
        items = [n for n in items if group in n.groups]
    if label:
        items = [n for n in items if label in n.labels or label in [f"{k}={v}" for k, v in n.labels.items()]]

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = items[start:end]

    return APIResponse(
        code=0,
        message="success",
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [n.dict() for n in page_items]
        }
    )

@app.get("/api/v1/nodes/{node_id}", response_model=APIResponse)
async def get_node(
    node_id: str,
    authorization: str = Header(None)
):
    await verify_api_key(authorization)

    node = NODES_DB.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="节点不存在")

    return APIResponse(
        code=0,
        message="success",
        data=node.dict()
    )

@app.post("/api/v1/nodes", response_model=APIResponse)
async def create_node(
    node: Node,
    authorization: str = Header(None)
):
    await verify_api_key(authorization)

    if node.id in NODES_DB:
        raise HTTPException(status_code=400, detail="节点已存在")

    node.created_at = datetime.now()
    node.updated_at = datetime.now()
    NODES_DB[node.id] = node

    return APIResponse(
        code=0,
        message="success",
        data=node.dict()
    )

@app.put("/api/v1/nodes/{node_id}", response_model=APIResponse)
async def update_node(
    node_id: str,
    node: Node,
    authorization: str = Header(None)
):
    await verify_api_key(authorization)

    if node_id not in NODES_DB:
        raise HTTPException(status_code=404, detail="节点不存在")

    node.updated_at = datetime.now()
    NODES_DB[node_id] = node

    return APIResponse(
        code=0,
        message="success",
        data=node.dict()
    )

@app.delete("/api/v1/nodes/{node_id}", response_model=APIResponse)
async def delete_node(
    node_id: str,
    authorization: str = Header(None)
):
    await verify_api_key(authorization)

    if node_id not in NODES_DB:
        raise HTTPException(status_code=404, detail="节点不存在")

    del NODES_DB[node_id]

    return APIResponse(
        code=0,
        message="success",
        data=None
    )

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**启动服务：**

```bash
# 设置 API Key
export API_KEY="sk-xxxxxxxxxxxxxxxx"

# 启动服务
python cmdb_server.py

# 或者使用 uvicorn
uvicorn cmdb_server:app --host 0.0.0.0 --port 8000 --reload
```

**测试 API：**

```bash
# 获取节点列表
curl -X GET "http://localhost:8000/api/v1/nodes" \
  -H "Authorization: Bearer sk-xxxxxxxxxxxxxxxx"

# 获取单个节点
curl -X GET "http://localhost:8000/api/v1/nodes/node-001" \
  -H "Authorization: Bearer sk-xxxxxxxxxxxxxxxx"

# 按名称过滤
curl -X GET "http://localhost:8000/api/v1/nodes?name=web" \
  -H "Authorization: Bearer sk-xxxxxxxxxxxxxxxx"

# 按分组过滤
curl -X GET "http://localhost:8000/api/v1/nodes?group=web" \
  -H "Authorization: Bearer sk-xxxxxxxxxxxxxxxx"
```