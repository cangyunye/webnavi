-- 枚举项表迁移脚本
-- 创建时间: 2024
-- 说明: 用于管理系统中的枚举值，如环境类型、数据库类型等

-- 创建 enum_items 表
CREATE TABLE IF NOT EXISTS enum_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enum_type VARCHAR(50) NOT NULL,
    enum_value VARCHAR(50) NOT NULL,
    enum_label VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    sort_order INT DEFAULT 0,
    is_active TINYINT DEFAULT 1,
    color VARCHAR(20),
    icon VARCHAR(50),
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_enum_type (enum_type),
    UNIQUE KEY uk_enum_type_value (enum_type, enum_value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入默认枚举值数据

-- 环境类型
INSERT INTO enum_items (enum_type, enum_value, enum_label, sort_order, color, icon) VALUES
('environment', 'prod', '生产环境', 1, '#ef4444', '🚨'),
('environment', 'test', '测试环境', 2, '#a855f7', '🧪'),
('environment', 'dev', '开发环境', 3, '#3b82f6', '💻'),
('environment', 'staging', '预发环境', 4, '#f59e0b', '🚀');

-- 数据库类型
INSERT INTO enum_items (enum_type, enum_value, enum_label, icon) VALUES
('db_type', 'MySQL', 'MySQL', '🗄️'),
('db_type', 'PostgreSQL', 'PostgreSQL', '🐘'),
('db_type', 'Redis', 'Redis', '⚡'),
('db_type', 'MongoDB', 'MongoDB', '🍃'),
('db_type', 'Elasticsearch', 'Elasticsearch', '🔍'),
('db_type', 'ClickHouse', 'ClickHouse', '🏠'),
('db_type', 'SQLite', 'SQLite', '📱'),
('db_type', 'SQL Server', 'SQL Server', '🪟'),
('db_type', 'Oracle', 'Oracle', '🔶'),
('db_type', 'MariaDB', 'MariaDB', '⭐');

-- 资源类型
INSERT INTO enum_items (enum_type, enum_value, enum_label, icon) VALUES
('resource_type', 'dev_machine', '研发机器', '🖥️'),
('resource_type', 'db_instance', '数据库实例', '🗄️');

-- 节点状态
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('node_status', 'active', '活跃', '#22c55e'),
('node_status', 'inactive', '非活跃', '#9ca3af'),
('node_status', 'maintenance', '维护中', '#f59e0b');

-- 通用状态
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('general_status', 'online', '在线', '#22c55e'),
('general_status', 'offline', '离线', '#9ca3af'),
('general_status', 'pending', '待处理', '#f59e0b'),
('general_status', 'error', '错误', '#ef4444');

-- 用户角色
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('user_role', 'admin', '管理员', '#ef4444'),
('user_role', 'registered', '注册用户', '#3b82f6'),
('user_role', 'guest', '访客', '#9ca3af');

-- 权限类型
INSERT INTO enum_items (enum_type, enum_value, enum_label) VALUES
('permission_type', 'view', '查看'),
('permission_type', 'edit', '编辑'),
('permission_type', 'delete', '删除'),
('permission_type', 'manage', '管理');

-- 操作系统类型
INSERT INTO enum_items (enum_type, enum_value, enum_label, icon) VALUES
('os_type', 'Linux', 'Linux', '🐧'),
('os_type', 'Windows', 'Windows', '🪟'),
('os_type', 'macOS', 'macOS', '🍎'),
('os_type', 'CentOS', 'CentOS', '🔴'),
('os_type', 'Ubuntu', 'Ubuntu', '🟠'),
('os_type', 'Debian', 'Debian', '🔵'),
('os_type', 'Red Hat', 'Red Hat', '🟢');

-- 告警级别
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('alert_level', 'critical', '严重', '#ef4444'),
('alert_level', 'warning', '警告', '#f59e0b'),
('alert_level', 'info', '信息', '#3b82f6'),
('alert_level', 'debug', '调试', '#9ca3af');

-- 日志级别
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('log_level', 'ERROR', '错误', '#ef4444'),
('log_level', 'WARN', '警告', '#f59e0b'),
('log_level', 'INFO', '信息', '#3b82f6'),
('log_level', 'DEBUG', '调试', '#9ca3af'),
('log_level', 'TRACE', '跟踪', '#6b7280');
