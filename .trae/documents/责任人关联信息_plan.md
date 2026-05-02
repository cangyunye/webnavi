# 责任人关联信息功能实现计划

## 功能需求

为数据库和研发机器增加责任人关联信息，实现：
- 确认机器负责人是谁
- 机器归属组织是哪里
- 支持查询某个责任人的所有负责资源

## 数据库设计

### 新增表

#### 1. `organizations` - 组织表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| name | VARCHAR(100) | 组织名称 |
| description | TEXT | 组织描述 |
| parent_id | INT | 上级组织ID（可为空，支持多级） |
| create_time | DATETIME | 创建时间 |

#### 2. `owners` - 责任人表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| username | VARCHAR(50) | 责任人姓名 |
| email | VARCHAR(100) | 邮箱 |
| phone | VARCHAR(20) | 电话 |
| organization_id | INT | 所属组织（外键） |
| create_time | DATETIME | 创建时间 |

#### 3. 修改现有表

**dev_machines 表新增字段**：
- `owner_id` - 责任人ID（外键，可为空）
- `organization_id` - 归属组织ID（外键，可为空）

**db_instances 表新增字段**：
- `owner_id` - 责任人ID（外键，可为空）
- `organization_id` - 归属组织ID（外键，可为空）

## 文件变更列表

### 数据库
- `sql/init.sql` - 新增 organizations、owners 表，更新 dev_machines、db_instances 表结构，添加示例数据

### 后端
- `backend/models.py` - 新增 Organization、Owner 模型，更新 DevMachine、DbInstance 模型
- `backend/schemas.py` - 新增 OrganizationResponse、OwnerResponse schemas，更新 DevMachineResponse、DbInstanceResponse
- `backend/routers/resources.py` - 新增组织列表、责任人列表 API
- `frontend/js/app.js` - 在表格中显示责任人和组织信息
- `frontend/css/style.css` - 添加相关样式

### API 变更

#### 新增接口
- `GET /api/organizations` - 获取组织列表
- `GET /api/owners` - 获取责任人列表
- `GET /api/owners/{owner_id}` - 获取责任人详情
- `GET /api/owners/{owner_id}/resources` - 获取责任人负责的所有资源

## 实现步骤

### Phase 1: 数据库
1. 更新 `sql/init.sql` 创建 organizations 和 owners 表
2. 为 dev_machines 和 db_instances 表添加外键字段
3. 插入示例数据

### Phase 2: 后端模型
1. 更新 `backend/models.py` 添加 Organization 和 Owner 模型
2. 更新 DevMachine 和 DbInstance 模型添加关联字段
3. 更新 `backend/schemas.py` 添加相关 schemas

### Phase 3: API
1. 在 `routers/resources.py` 中添加组织和责任人查询接口
2. 更新研发机器和数据库实例查询返回责任人信息

### Phase 4: 前端
1. 更新 `frontend/js/app.js` 在表格中显示责任人和组织
2. 更新 `frontend/css/style.css` 添加相关样式
