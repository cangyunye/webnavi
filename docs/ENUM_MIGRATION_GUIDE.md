# 枚举管理模块数据迁移指南

## 概述

本文档描述如何将系统中硬编码的枚举值迁移到新的 `enum_items` 表中。

## 迁移步骤

### 步骤 1：创建枚举表

执行 SQL 迁移脚本创建 `enum_items` 表并插入默认数据：

```bash
# 使用 MySQL 命令行执行
mysql -u your_user -p your_database < sql/enum_items_migration.sql

# 或者使用 Python 自动创建（推荐）
cd backend
source .venv/bin/activate
python -c "
from database import engine, Base
Base.metadata.create_all(engine)
print('Tables created successfully')
"
```

### 步骤 2：验证数据

验证枚举表是否创建成功：

```sql
-- 查看所有枚举类型
SELECT DISTINCT enum_type FROM enum_items;

-- 查看环境类型枚举值
SELECT * FROM enum_items WHERE enum_type = 'environment';

-- 查看数据库类型枚举值
SELECT * FROM enum_items WHERE enum_type = 'db_type';
```

### 步骤 3：前端代码迁移

#### 3.1 新增枚举数据缓存函数

在 `frontend/js/app.js` 中添加：

```javascript
let enumCache = {};

async function loadEnumOptions(enumType) {
    if (enumCache[enumType]) {
        return enumCache[enumType];
    }
    
    try {
        const options = await apiRequest(`${API_BASE}/enum-items/${enumType}/options`);
        enumCache[enumType] = options;
        return options;
    } catch (e) {
        console.error(`Failed to load enum ${enumType}:`, e);
        return [];
    }
}

function getEnumLabel(enumType, value) {
    if (!enumCache[enumType]) return value;
    const item = enumCache[enumType].find(e => e.value === value);
    return item ? item.label : value;
}
```

#### 3.2 替换硬编码的枚举值

**原代码（硬编码）：**
```javascript
// 环境类型下拉框
<select class="form-input" id="machine-environment">
    <option value="dev">开发环境</option>
    <option value="test">测试环境</option>
    <option value="prod">生产环境</option>
</select>
```

**新代码（动态加载）：**
```javascript
// 在加载表单时动态生成
const envOptions = await loadEnumOptions('environment');
const envSelect = document.getElementById('machine-environment');
envSelect.innerHTML = envOptions.map(opt => 
    `<option value="${opt.value}">${opt.label}</option>`
).join('');
```

### 步骤 4：后端代码迁移（可选）

#### 4.1 添加枚举验证依赖

在需要验证枚举值的地方，可以添加如下依赖：

```python
from fastapi import HTTPException
from sqlalchemy.orm import Session

def validate_enum_value(db: Session, enum_type: str, value: str):
    """验证枚举值是否有效"""
    exists = db.query(EnumItem).filter(
        EnumItem.enum_type == enum_type,
        EnumItem.enum_value == value,
        EnumItem.is_active == 1
    ).first()
    
    if not exists:
        raise HTTPException(
            status_code=400,
            detail=f"无效的 {enum_type} 值: {value}"
        )
    return True
```

#### 4.2 更新现有模型（可选）

如果需要，可以为现有字段添加外键约束：

```sql
-- 示例：为 dev_machines.environment 添加外键约束（可选）
ALTER TABLE dev_machines 
ADD CONSTRAINT fk_env 
FOREIGN KEY (environment) 
REFERENCES enum_items(enum_value) 
ON UPDATE CASCADE;
```

> **注意**：添加外键约束前需要确保所有现有数据都在枚举表中有对应值。

## 向后兼容性

### 方案 A：双轨运行（推荐）

1. **前端**：同时支持硬编码和动态加载
2. **后端**：接受旧值，逐步迁移
3. **数据**：新表中的默认值与旧值保持一致

### 方案 B：一次性迁移

1. **停服迁移**：停止服务，执行迁移脚本
2. **数据校验**：验证所有枚举字段的值都在新表中存在
3. **更新代码**：移除所有硬编码枚举值

## 回滚方案

如果迁移出现问题，可以使用以下步骤回滚：

1. **删除枚举表**：
   ```sql
   DROP TABLE IF EXISTS enum_items;
   ```

2. **恢复代码**：恢复到迁移前的代码版本
3. **重启服务**：服务恢复到迁移前状态

## 迁移验证清单

- [ ] `enum_items` 表已创建
- [ ] 默认枚举数据已插入
- [ ] 前端已集成枚举 API
- [ ] 后端 API 测试通过
- [ ] 现有数据验证通过
- [ ] 用户界面测试通过

## API 使用示例

### 获取环境类型选项

```bash
curl -X GET "http://localhost:8000/api/enum-items/environment/options" \
  -H "Authorization: Bearer <your_token>"
```

**响应：**
```json
[
  {"value": "prod", "label": "生产环境"},
  {"value": "test", "label": "测试环境"},
  {"value": "dev", "label": "开发环境"},
  {"value": "staging", "label": "预发环境"}
]
```

### 获取完整枚举信息（含颜色、图标）

```bash
curl -X GET "http://localhost:8000/api/enum-items/environment/options-full" \
  -H "Authorization: Bearer <your_token>"
```

**响应：**
```json
[
  {
    "value": "prod",
    "label": "生产环境",
    "color": "#ef4444",
    "icon": "🚨",
    "description": null
  },
  ...
]
```

### 创建新枚举项

```bash
curl -X POST "http://localhost:8000/api/enum-items" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "enum_type": "environment",
    "enum_value": "sandbox",
    "enum_label": "沙箱环境",
    "color": "#10b981",
    "icon": "🏖️"
  }'
```

## 注意事项

1. **权限控制**：枚举管理仅对管理员开放
2. **数据一致性**：删除或修改枚举值前需确认没有业务数据引用
3. **缓存策略**：前端建议定时刷新枚举缓存
4. **默认值**：新增枚举项时 `sort_order` 默认值为 0，`is_active` 默认值为 1
