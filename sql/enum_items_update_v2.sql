-- 枚举项表升级脚本 v2
-- 创建时间: 2024
-- 说明: 补充缺失的数据库类型、环境类型和归属组织枚举值

USE resource_nav;

-- ==================== 新增数据库类型 ====================
INSERT INTO enum_items (enum_type, enum_value, enum_label, icon) VALUES
('db_type', 'OceanBase', 'OceanBase', '🌊'),
('db_type', 'PolarDB', 'PolarDB', '🐬'),
('db_type', 'TiDB', 'TiDB', '🌙'),
('db_type', 'CockroachDB', 'CockroachDB', '🦗'),
('db_type', 'StarRocks', 'StarRocks', '⭐'),
('db_type', 'Doris', 'Apache Doris', '🌰')
ON DUPLICATE KEY UPDATE enum_label = VALUES(enum_label), icon = VALUES(icon);

-- ==================== 新增环境类型 ====================
INSERT INTO enum_items (enum_type, enum_value, enum_label, sort_order, color, icon) VALUES
('environment', 'sandbox', '沙箱环境', 5, '#10b981', '🏖️'),
('environment', 'local', '本地环境', 6, '#6b7280', '💻'),
('environment', 'uat', '用户验收环境', 7, '#8b5cf6', '🔮'),
('environment', 'dr', '容灾环境', 8, '#f97316', '🛡️')
ON DUPLICATE KEY UPDATE enum_label = VALUES(enum_label), sort_order = VALUES(sort_order), color = VALUES(color), icon = VALUES(icon);

-- ==================== 新增归属组织 ====================
INSERT INTO enum_items (enum_type, enum_value, enum_label) VALUES
('organization', 'infrastructure', '基础架构部'),
('organization', 'frontend', '前端研发组'),
('organization', 'backend', '后端研发组'),
('organization', 'ai_lab', 'AI实验室'),
('organization', 'data_platform', '数据平台部'),
('organization', 'cloud', '云计算中心'),
('organization', 'security', '安全团队'),
('organization', 'qa', '质量保障组'),
('organization', 'ops', '运维组'),
('organization', 'product', '产品组')
ON DUPLICATE KEY UPDATE enum_label = VALUES(enum_label);

SELECT '枚举数据升级完成' AS result;
