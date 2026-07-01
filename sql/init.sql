SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS resource_nav DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE resource_nav;

DROP TABLE IF EXISTS resource_themes;
DROP TABLE IF EXISTS api_key_logs;
DROP TABLE IF EXISTS api_keys;
DROP TABLE IF EXISTS credentials;
DROP TABLE IF EXISTS nodes;
DROP TABLE IF EXISTS enum_items;
DROP TABLE IF EXISTS resources;
DROP TABLE IF EXISTS db_instances;
DROP TABLE IF EXISTS dev_machines;
DROP TABLE IF EXISTS owners;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(100) NOT NULL,
    sort_order INT DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE organizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE owners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    organization_id INT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dev_machines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ip VARCHAR(50) NOT NULL,
    port INT DEFAULT 22,
    hostname VARCHAR(100),
    cpu VARCHAR(50),
    memory VARCHAR(50),
    disk VARCHAR(100),
    os VARCHAR(100),
    status VARCHAR(20) DEFAULT 'online',
    environment VARCHAR(50) DEFAULT 'dev',
    description TEXT,
    owner_id INT,
    organization_id INT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owners(id),
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE db_instances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    db_type VARCHAR(50) NOT NULL,
    version VARCHAR(50),
    ip VARCHAR(50) NOT NULL,
    port INT DEFAULT 3306,
    charset VARCHAR(20) DEFAULT 'utf8mb4',
    status VARCHAR(20) DEFAULT 'online',
    environment VARCHAR(50) DEFAULT 'dev',
    description TEXT,
    owner_id INT,
    organization_id INT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owners(id),
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(500) NOT NULL,
    description TEXT,
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE resource_themes (
    resource_id INT NOT NULL PRIMARY KEY,
    theme_key   VARCHAR(50) NOT NULL DEFAULT 'default',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20) DEFAULT 'guest',
    is_active TINYINT DEFAULT 1,
    can_edit TINYINT DEFAULT 0,
    can_delete TINYINT DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,
    resource_id INT NOT NULL,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    description TEXT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE api_keys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    key_name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    key_prefix VARCHAR(20) NOT NULL,
    scopes JSON DEFAULT ('[]'),
    is_active TINYINT DEFAULT 1,
    expires_at DATETIME,
    last_used_at DATETIME,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_key_prefix (key_prefix)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE api_key_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_key_id INT NOT NULL,
    user_id INT NOT NULL,
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(20) NOT NULL,
    ip_address VARCHAR(100),
    user_agent VARCHAR(500),
    request_body JSON,
    response_status INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (api_key_id) REFERENCES api_keys(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_api_key_id (api_key_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE enum_items (
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

CREATE TABLE nodes (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hostname VARCHAR(100),
    address VARCHAR(50) NOT NULL,
    port INT DEFAULT 22,
    user VARCHAR(50) DEFAULT 'root',
    status VARCHAR(20) DEFAULT 'active',
    `groups` JSON,
    labels JSON,
    ssh_key VARCHAR(500),
    ssh_password VARCHAR(255),
    proxy_jump VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
USE resource_nav;

-- 分类
INSERT INTO categories (name, icon, sort_order) VALUES
('学习', 'icon-study', 1),
('数据库', 'icon-database', 2),
('研发机器', 'icon-dev-machine', 3),
('AI', 'icon-ai', 4),
('测试', 'icon-test', 5),
('软件资源', 'icon-software', 6),
('运维', 'icon-ops', 7),
('工具', 'icon-tools', 8);

-- 组织
INSERT INTO organizations (name, description, parent_id) VALUES
('基础架构部', '负责公司基础架构建设和运维', NULL),
('前端研发组', '负责前端技术研发', NULL),
('后端研发组', '负责后端服务研发', NULL),
('AI实验室', '负责人工智能技术研发', NULL),
('数据平台部', '负责数据平台建设', NULL),
('云计算中心', '负责云资源管理', NULL);

-- 责任人
INSERT INTO owners (username, email, phone, organization_id) VALUES
('张三', 'zhangsan@example.com', '13800138001', 1),
('李四', 'lisi@example.com', '13800138002', 2),
('王五', 'wangwu@example.com', '13800138003', 3),
('赵六', 'zhaoliu@example.com', '13800138004', 4),
('钱七', 'qianqi@example.com', '13800138005', 5),
('孙八', 'sunba@example.com', '13800138006', 6),
('周九', 'zhoujiu@example.com', '13800138007', 1),
('吴十', 'wushi@example.com', '13800138008', 3);

-- 研发机器
INSERT INTO dev_machines (name, ip, port, hostname, cpu, memory, disk, os, status, environment, description, owner_id, organization_id) VALUES
('开发服务器-01', '192.168.1.101', 22, 'dev-server-01', '8核 Intel Xeon', '16GB', '500GB SSD', 'Ubuntu 22.04 LTS', 'online', 'dev', '开发测试环境主服务器', 1, 1),
('开发服务器-02', '192.168.1.102', 22, 'dev-server-02', '16核 Intel Xeon', '32GB', '1TB SSD', 'CentOS 7.9', 'online', 'dev', '开发测试环境副服务器', 3, 3),
('测试服务器-01', '192.168.1.201', 22, 'test-server-01', '8核 AMD Ryzen 7', '16GB', '500GB SSD', 'Ubuntu 22.04 LTS', 'online', 'test', '功能测试服务器', 2, 2),
('测试服务器-02', '192.168.1.202', 22, 'test-server-02', '8核 Intel Xeon', '16GB', '500GB SSD', 'Debian 11', 'online', 'test', '性能测试服务器', 2, 2),
('预生产服务器-01', '192.168.1.301', 22, 'pre-prod-01', '32核 Intel Xeon', '64GB', '2TB SSD', 'Ubuntu 22.04 LTS', 'online', 'prod', '预生产环境', 7, 6),
('生产服务器-01', '192.168.1.101', 22, 'prod-server-01', '64核 Intel Xeon', '128GB', '4TB SSD', 'CentOS 8', 'online', 'prod', '生产环境主服务器', 7, 6),
('生产服务器-02', '192.168.1.102', 22, 'prod-server-02', '64核 Intel Xeon', '128GB', '4TB SSD', 'CentOS 8', 'online', 'prod', '生产环境副服务器', 7, 6),
('构建服务器', '192.168.1.50', 22, 'build-server', '32核 Intel Xeon', '64GB', '2TB HDD', 'Ubuntu 22.04 LTS', 'online', 'dev', 'CI/CD构建服务器', 1, 1),
('GPU服务器', '192.168.1.150', 22, 'gpu-server-01', '32核 Intel Xeon + 4x RTX 3090', '128GB', '2TB NVMe', 'Ubuntu 22.04 LTS', 'online', 'dev', 'GPU深度学习服务器', 4, 4),
('日志服务器', '192.168.1.60', 22, 'log-server', '16核 Intel Xeon', '32GB', '4TB HDD', 'Ubuntu 22.04 LTS', 'online', 'dev', '日志收集服务器', 5, 5),
('缓存服务器', '192.168.1.70', 22, 'cache-server', '8核 Intel Xeon', '16GB', '256GB SSD', 'Ubuntu 22.04 LTS', 'online', 'dev', 'Redis缓存服务器', 6, 6),
('负载均衡器', '192.168.1.80', 22, 'lb-server', '8核 Intel Xeon', '8GB', '128GB SSD', 'Ubuntu 22.04 LTS', 'online', 'prod', 'Nginx负载均衡服务器', 6, 6),
('故障服务器-01', '192.168.1.250', 22, 'failed-server-01', '8核 Intel Xeon', '16GB', '500GB SSD', 'Ubuntu 22.04 LTS', 'error', 'dev', '硬件故障，待修复', NULL, NULL),
('待审批服务器-01', '192.168.1.251', 22, 'pending-server-01', '8核 Intel Xeon', '16GB', '500GB SSD', 'CentOS 9', 'pending', 'test', '新购服务器等待审批', NULL, NULL),
('待审批服务器-02', '192.168.1.252', 22, 'pending-server-02', '16核 AMD EPYC', '32GB', '1TB SSD', 'Rocky Linux 9', 'pending', 'staging', '预发布环境等待上线', NULL, NULL),
('离线服务器-01', '192.168.1.253', 22, 'offline-server-01', '8核 Intel Xeon', '16GB', '500GB HDD', 'CentOS 7', 'offline', 'dev', '已退役，待下架', NULL, NULL),
('备用机器-01', '192.168.1.254', 22, 'spare-server-01', '16核 Intel Xeon', '32GB', '1TB SSD', 'Ubuntu 22.04 LTS', 'offline', 'prod', '备用机器，冷备状态', NULL, NULL);

-- 数据库实例
INSERT INTO db_instances (name, db_type, version, ip, port, charset, status, environment, description, owner_id, organization_id) VALUES
('MySQL-主库-dev', 'MySQL', '8.0.35', '192.168.2.101', 3306, 'utf8mb4', 'online', 'dev', '开发环境MySQL主库', 1, 1),
('MySQL-从库-dev', 'MySQL', '8.0.35', '192.168.2.102', 3306, 'utf8mb4', 'online', 'dev', '开发环境MySQL从库', 1, 1),
('MySQL-主库-test', 'MySQL', '8.0.35', '192.168.2.201', 3306, 'utf8mb4', 'online', 'test', '测试环境MySQL主库', 2, 2),
('MySQL-主库-prod', 'MySQL', '8.0.35', '192.168.2.301', 3306, 'utf8mb4', 'online', 'prod', '生产环境MySQL主库', 7, 6),
('PostgreSQL-dev', 'PostgreSQL', '16.1', '192.168.2.110', 5432, 'UTF8', 'online', 'dev', '开发环境PostgreSQL', 3, 3),
('PostgreSQL-prod', 'PostgreSQL', '16.1', '192.168.2.310', 5432, 'UTF8', 'online', 'prod', '生产环境PostgreSQL', 7, 6),
('Redis-dev', 'Redis', '7.2.3', '192.168.2.120', 6379, 'UTF8', 'online', 'dev', '开发环境Redis缓存', 6, 6),
('Redis-prod', 'Redis', '7.2.3', '192.168.2.320', 6379, 'UTF8', 'online', 'prod', '生产环境Redis缓存', 6, 6),
('MongoDB-dev', 'MongoDB', '7.0.5', '192.168.2.130', 27017, 'UTF8', 'online', 'dev', '开发环境MongoDB', 5, 5),
('Elasticsearch-dev', 'Elasticsearch', '8.11.3', '192.168.2.140', 9200, 'UTF8', 'online', 'dev', '开发环境搜索引擎', 5, 5),
('ClickHouse-dev', 'ClickHouse', '23.11.2', '192.168.2.150', 9000, 'UTF8', 'online', 'dev', '开发环境OLAP数据库', 5, 5),
('故障MySQL', 'MySQL', '8.0', '192.168.2.200', 3306, 'utf8mb4', 'error', 'dev', '数据库异常，IO 挂载失败', NULL, NULL),
('待审批PG', 'PostgreSQL', '16', '192.168.2.201', 5432, 'UTF8', 'pending', 'test', '新部署待验收', NULL, NULL),
('待审批Redis', 'Redis', '7.2', '192.168.2.202', 6379, 'UTF8', 'pending', 'staging', '缓存实例等待上线', NULL, NULL),
('离线MySQL', 'MySQL', '8.0', '192.168.2.203', 3306, 'utf8mb4', 'offline', 'dev', '已废弃待清理', NULL, NULL),
('备用Mongo', 'MongoDB', '7.0', '192.168.2.204', 27017, 'UTF8', 'offline', 'prod', '冷备数据库', NULL, NULL);

-- 资源
INSERT INTO resources (category_id, name, url, description, status) VALUES
(1, 'GitHub', 'https://github.com', '全球最大的代码托管平台', 1),
(1, 'Stack Overflow', 'https://stackoverflow.com', '开发者问答社区', 1),
(1, 'MDN Web Docs', 'https://developer.mozilla.org', 'Web技术官方文档', 1),
(1, '菜鸟教程', 'https://www.runoob.com', '编程学习教程网站', 1),
(1, 'LeetCode', 'https://leetcode.com', '算法刷题平台', 1),
(1, 'Codecademy', 'https://www.codecademy.com', '在线编程学习平台', 1),
(4, 'OpenAI', 'https://openai.com', '人工智能研究公司', 1),
(4, 'Hugging Face', 'https://huggingface.co', 'AI模型开源社区', 1),
(4, 'Stable Diffusion', 'https://stability.ai', 'AI图片生成模型', 1),
(4, 'MidJourney', 'https://www.midjourney.com', 'AI绘画工具', 1),
(4, 'Claude', 'https://anthropic.com', 'Anthropic AI助手', 1),
(4, 'Perplexity', 'https://perplexity.ai', 'AI搜索引擎', 1),
(6, 'VS Code', 'https://code.visualstudio.com', '轻量级代码编辑器', 1),
(6, 'Docker', 'https://www.docker.com', '容器化应用平台', 1),
(6, 'Notion', 'https://www.notion.so', '笔记与协作工具', 1),
(6, 'Figma', 'https://www.figma.com', 'UI设计协作工具', 1),
(6, 'Chrome', 'https://www.google.com/chrome', 'Google浏览器', 1),
(8, 'wttr.in', 'https://wttr.in', '命令行风格的天气预报工具，支持 curl 直接调用', 1),
(8, 'Public APIs', 'https://github.com/public-apis/public-apis', '开源 API 集合，收录各种免费 API 接口', 1),
(8, 'Papers With Code', 'https://paperswithcode.com', '机器学习论文 + 数据集 + 代码实现汇总', 1),
(8, 'Hugging Face Datasets', 'https://huggingface.co/datasets', '开源机器学习数据集仓库', 1),
(8, 'DevDocs', 'https://devdocs.io', '开发者文档聚合查询工具', 1),
(5, 'Postman', 'https://postman.com', 'API 测试与调试工具', 1),
(5, 'Selenium', 'https://selenium.dev', '浏览器自动化测试框架', 1),
(5, 'Jest', 'https://jestjs.io', 'JavaScript 测试框架', 1),
(5, 'JMeter', 'https://jmeter.apache.org', '性能测试与负载测试工具', 1),
(5, 'Swagger', 'https://swagger.io', 'API 文档与测试工具', 1),
(7, 'Grafana', 'https://grafana.com', '监控与可视化平台', 1),
(7, 'Prometheus', 'https://prometheus.io', '系统监控与告警套件', 1),
(7, 'Jenkins', 'https://jenkins.io', 'CI/CD 持续集成平台', 1),
(7, 'Ansible', 'https://ansible.com', '配置管理与自动化工具', 1),
(7, 'ELK Stack', 'https://elastic.co', '日志采集与分析平台', 1);

-- 用户
INSERT INTO users (username, email, password_hash, role, is_active, can_edit, can_delete) VALUES
('admin', 'admin@example.com', '$2b$12$QL0LG1zvAemsOOS9qoemnundznMTN/E7vs8Lqc2IwSpXaKFf7mikK', 'admin', 1, 1, 1);

-- 凭据
INSERT INTO credentials (resource_type, resource_id, username, password, description) VALUES
('dev_machine', 1, 'root', 'dev12345', '开发服务器 root 用户'),
('dev_machine', 1, 'admin', 'adminPass@1', '开发服务器管理员'),
('dev_machine', 3, 'admin', 'testAdmin01', '测试服务器管理员'),
('db_instance', 1, 'root', 'mysqlRoot@1', 'MySQL dev 主库 root'),
('db_instance', 1, 'dev_user', 'devPass@123', 'MySQL dev 开发用户'),
('db_instance', 4, 'root', 'prodMysqlRoot@1', '生产 MySQL root 用户');

-- 枚举项: 环境类型
INSERT INTO enum_items (enum_type, enum_value, enum_label, sort_order, color, icon) VALUES
('environment', 'prod', '生产环境', 1, '#ef4444', '🚨'),
('environment', 'test', '测试环境', 2, '#a855f7', '🧪'),
('environment', 'dev', '开发环境', 3, '#3b82f6', '💻'),
('environment', 'staging', '预发环境', 4, '#f59e0b', '🚀'),
('environment', 'sandbox', '沙箱环境', 5, '#10b981', '🏖️'),
('environment', 'local', '本地环境', 6, '#6b7280', '💻'),
('environment', 'uat', '用户验收环境', 7, '#8b5cf6', '🔮'),
('environment', 'dr', '容灾环境', 8, '#f97316', '🛡️');

-- 枚举项: 数据库类型
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
('db_type', 'MariaDB', 'MariaDB', '⭐'),
('db_type', 'OceanBase', 'OceanBase', '🌊'),
('db_type', 'PolarDB', 'PolarDB', '🐬'),
('db_type', 'TiDB', 'TiDB', '🌙'),
('db_type', 'CockroachDB', 'CockroachDB', '🦗'),
('db_type', 'StarRocks', 'StarRocks', '⭐'),
('db_type', 'Doris', 'Apache Doris', '🌰');

-- 枚举项: 资源类型
INSERT INTO enum_items (enum_type, enum_value, enum_label, icon) VALUES
('resource_type', 'dev_machine', '研发机器', '🖥️'),
('resource_type', 'db_instance', '数据库实例', '🗄️');

-- 枚举项: 组织
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
('organization', 'product', '产品组');

-- 枚举项: 节点状态
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('node_status', 'active', '活跃', '#22c55e'),
('node_status', 'inactive', '非活跃', '#9ca3af'),
('node_status', 'maintenance', '维护中', '#f59e0b');

-- 枚举项: 通用状态
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('general_status', 'online', '在线', '#22c55e'),
('general_status', 'offline', '离线', '#9ca3af'),
('general_status', 'pending', '待处理', '#f59e0b'),
('general_status', 'error', '错误', '#ef4444');

-- 枚举项: 用户角色
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('user_role', 'admin', '管理员', '#ef4444'),
('user_role', 'registered', '注册用户', '#3b82f6'),
('user_role', 'guest', '访客', '#9ca3af');

-- 枚举项: 权限类型
INSERT INTO enum_items (enum_type, enum_value, enum_label) VALUES
('permission_type', 'view', '查看'),
('permission_type', 'edit', '编辑'),
('permission_type', 'delete', '删除'),
('permission_type', 'manage', '管理');

-- 枚举项: 操作系统类型
INSERT INTO enum_items (enum_type, enum_value, enum_label, icon) VALUES
('os_type', 'Linux', 'Linux', '🐧'),
('os_type', 'Windows', 'Windows', '🪟'),
('os_type', 'macOS', 'macOS', '🍎'),
('os_type', 'CentOS', 'CentOS', '🔴'),
('os_type', 'Ubuntu', 'Ubuntu', '🟠'),
('os_type', 'Debian', 'Debian', '🔵'),
('os_type', 'Red Hat', 'Red Hat', '🟢');

-- 枚举项: 告警级别
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('alert_level', 'critical', '严重', '#ef4444'),
('alert_level', 'warning', '警告', '#f59e0b'),
('alert_level', 'info', '信息', '#3b82f6'),
('alert_level', 'debug', '调试', '#9ca3af');

-- 枚举项: 日志级别
INSERT INTO enum_items (enum_type, enum_value, enum_label, color) VALUES
('log_level', 'ERROR', '错误', '#ef4444'),
('log_level', 'WARN', '警告', '#f59e0b'),
('log_level', 'INFO', '信息', '#3b82f6'),
('log_level', 'DEBUG', '调试', '#9ca3af'),
('log_level', 'TRACE', '跟踪', '#6b7280');

-- 枚举项: 资源主题
INSERT INTO enum_items (enum_type, enum_value, enum_label, sort_order, color, icon) VALUES
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
