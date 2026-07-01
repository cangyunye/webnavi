-- 资源主题迁移脚本
-- 创建时间: 2025
-- 说明: 为资源卡片添加独立主题系统

-- 创建 resource_themes 表
CREATE TABLE IF NOT EXISTS resource_themes (
    resource_id INT NOT NULL PRIMARY KEY,
    theme_key   VARCHAR(50) NOT NULL DEFAULT 'default',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入资源主题枚举项
INSERT IGNORE INTO enum_items (enum_type, enum_value, enum_label, sort_order, color, icon) VALUES
('resource_theme', 'default', '云白', 0, '#ffffff', '☁️'),
('resource_theme', 'red', '高优先', 1, '#ef4444', '🔴'),
('resource_theme', 'blue', '频率中等', 2, '#3b82f6', '🔵'),
('resource_theme', 'green', '通用', 3, '#22c55e', '🟢'),
('resource_theme', 'yellow', '第三方工具', 4, '#eab308', '🟡'),
('resource_theme', 'purple', '自定义', 5, '#a855f7', '🟣'),
('resource_theme', 'orange', '重点项目', 6, '#f97316', '🟠'),
('resource_theme', 'teal', '内部服务', 7, '#14b8a6', '🩵'),
('resource_theme', 'pink', '待分类', 8, '#ec4899', '🩷'),
('resource_theme', 'gray', '归档', 9, '#6b7280', '⚪');
