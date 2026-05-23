SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS resource_nav DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE resource_nav;

DROP TABLE IF EXISTS credentials;
DROP TABLE IF EXISTS user_permissions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS resources;
DROP TABLE IF EXISTS db_instances;
DROP TABLE IF EXISTS dev_machines;
DROP TABLE IF EXISTS owners;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(100) NOT NULL,
    sort_order INT DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO categories (name, icon, sort_order) VALUES
('学习', 'icon-study', 1),
('数据库', 'icon-database', 2),
('研发机器', 'icon-dev-machine', 3),
('AI', 'icon-ai', 4),
('测试', 'icon-test', 5),
('软件资源', 'icon-software', 6),
('运维', 'icon-ops', 7);

CREATE TABLE organizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO organizations (name, description, parent_id) VALUES
('基础架构部', '负责公司基础架构建设和运维', NULL),
('前端研发组', '负责前端技术研发', NULL),
('后端研发组', '负责后端服务研发', NULL),
('AI实验室', '负责人工智能技术研发', NULL),
('数据平台部', '负责数据平台建设', NULL),
('云计算中心', '负责云资源管理', NULL);

CREATE TABLE owners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    organization_id INT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO owners (username, email, phone, organization_id) VALUES
('张三', 'zhangsan@example.com', '13800138001', 1),
('李四', 'lisi@example.com', '13800138002', 2),
('王五', 'wangwu@example.com', '13800138003', 3),
('赵六', 'zhaoliu@example.com', '13800138004', 4),
('钱七', 'qianqi@example.com', '13800138005', 5),
('孙八', 'sunba@example.com', '13800138006', 6),
('周九', 'zhoujiu@example.com', '13800138007', 1),
('吴十', 'wushi@example.com', '13800138008', 3);

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
    status TINYINT DEFAULT 1,
    environment VARCHAR(50) DEFAULT 'dev',
    description TEXT,
    owner_id INT,
    organization_id INT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owners(id),
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dev_machines (name, ip, port, hostname, cpu, memory, disk, os, status, environment, description, owner_id, organization_id) VALUES
('开发服务器-01', '192.168.1.101', 22, 'dev-server-01', '8核 Intel Xeon', '16GB', '500GB SSD', 'Ubuntu 22.04 LTS', 1, 'dev', '开发测试环境主服务器', 1, 1),
('开发服务器-02', '192.168.1.102', 22, 'dev-server-02', '16核 Intel Xeon', '32GB', '1TB SSD', 'CentOS 7.9', 1, 'dev', '开发测试环境副服务器', 3, 3),
('测试服务器-01', '192.168.1.201', 22, 'test-server-01', '8核 AMD Ryzen 7', '16GB', '500GB SSD', 'Ubuntu 22.04 LTS', 1, 'test', '功能测试服务器', 2, 2),
('测试服务器-02', '192.168.1.202', 22, 'test-server-02', '8核 Intel Xeon', '16GB', '500GB SSD', 'Debian 11', 1, 'test', '性能测试服务器', 2, 2),
('预生产服务器-01', '192.168.1.301', 22, 'pre-prod-01', '32核 Intel Xeon', '64GB', '2TB SSD', 'Ubuntu 22.04 LTS', 1, 'prod', '预生产环境', 7, 6),
('生产服务器-01', '192.168.1.101', 22, 'prod-server-01', '64核 Intel Xeon', '128GB', '4TB SSD', 'CentOS 8', 1, 'prod', '生产环境主服务器', 7, 6),
('生产服务器-02', '192.168.1.102', 22, 'prod-server-02', '64核 Intel Xeon', '128GB', '4TB SSD', 'CentOS 8', 1, 'prod', '生产环境副服务器', 7, 6),
('构建服务器', '192.168.1.50', 22, 'build-server', '32核 Intel Xeon', '64GB', '2TB HDD', 'Ubuntu 22.04 LTS', 1, 'dev', 'CI/CD构建服务器', 1, 1),
('GPU服务器', '192.168.1.150', 22, 'gpu-server-01', '32核 Intel Xeon + 4x RTX 3090', '128GB', '2TB NVMe', 'Ubuntu 22.04 LTS', 1, 'dev', 'GPU深度学习服务器', 4, 4),
('日志服务器', '192.168.1.60', 22, 'log-server', '16核 Intel Xeon', '32GB', '4TB HDD', 'Ubuntu 22.04 LTS', 1, 'dev', '日志收集服务器', 5, 5),
('缓存服务器', '192.168.1.70', 22, 'cache-server', '8核 Intel Xeon', '16GB', '256GB SSD', 'Ubuntu 22.04 LTS', 1, 'dev', 'Redis缓存服务器', 6, 6),
('负载均衡器', '192.168.1.80', 22, 'lb-server', '8核 Intel Xeon', '8GB', '128GB SSD', 'Ubuntu 22.04 LTS', 1, 'prod', 'Nginx负载均衡服务器', 6, 6);

CREATE TABLE db_instances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    db_type VARCHAR(50) NOT NULL,
    version VARCHAR(50),
    ip VARCHAR(50) NOT NULL,
    port INT DEFAULT 3306,
    charset VARCHAR(20) DEFAULT 'utf8mb4',
    status TINYINT DEFAULT 1,
    environment VARCHAR(50) DEFAULT 'dev',
    description TEXT,
    owner_id INT,
    organization_id INT,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owners(id),
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO db_instances (name, db_type, version, ip, port, charset, status, environment, description, owner_id, organization_id) VALUES
('MySQL-主库-dev', 'MySQL', '8.0.35', '192.168.2.101', 3306, 'utf8mb4', 1, 'dev', '开发环境MySQL主库', 1, 1),
('MySQL-从库-dev', 'MySQL', '8.0.35', '192.168.2.102', 3306, 'utf8mb4', 1, 'dev', '开发环境MySQL从库', 1, 1),
('MySQL-主库-test', 'MySQL', '8.0.35', '192.168.2.201', 3306, 'utf8mb4', 1, 'test', '测试环境MySQL主库', 2, 2),
('MySQL-主库-prod', 'MySQL', '8.0.35', '192.168.2.301', 3306, 'utf8mb4', 1, 'prod', '生产环境MySQL主库', 7, 6),
('PostgreSQL-dev', 'PostgreSQL', '16.1', '192.168.2.110', 5432, 'UTF8', 1, 'dev', '开发环境PostgreSQL', 3, 3),
('PostgreSQL-prod', 'PostgreSQL', '16.1', '192.168.2.310', 5432, 'UTF8', 1, 'prod', '生产环境PostgreSQL', 7, 6),
('Redis-dev', 'Redis', '7.2.3', '192.168.2.120', 6379, 'UTF8', 1, 'dev', '开发环境Redis缓存', 6, 6),
('Redis-prod', 'Redis', '7.2.3', '192.168.2.320', 6379, 'UTF8', 1, 'prod', '生产环境Redis缓存', 6, 6),
('MongoDB-dev', 'MongoDB', '7.0.5', '192.168.2.130', 27017, 'UTF8', 1, 'dev', '开发环境MongoDB', 5, 5),
('Elasticsearch-dev', 'Elasticsearch', '8.11.3', '192.168.2.140', 9200, 'UTF8', 1, 'dev', '开发环境搜索引擎', 5, 5),
('ClickHouse-dev', 'ClickHouse', '23.11.2', '192.168.2.150', 9000, 'UTF8', 1, 'dev', '开发环境OLAP数据库', 5, 5);

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
(6, 'Chrome', 'https://www.google.com/chrome', 'Google浏览器', 1);

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

INSERT INTO users (username, email, password_hash, role, is_active, can_edit, can_delete) VALUES
('admin', 'admin@example.com', '$2b$12$QL0LG1zvAemsOOS9qoemnundznMTN/E7vs8Lqc2IwSpXaKFf7mikK', 'admin', 1, 1, 1);

CREATE TABLE user_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT,
    permission_type VARCHAR(20) DEFAULT 'view',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
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

INSERT INTO credentials (resource_type, resource_id, username, password, description) VALUES
('dev_machine', 1, 'root', 'dev12345', '开发服务器 root 用户'),
('dev_machine', 1, 'admin', 'adminPass@1', '开发服务器管理员'),
('dev_machine', 3, 'admin', 'testAdmin01', '测试服务器管理员'),
('db_instance', 1, 'root', 'mysqlRoot@1', 'MySQL dev 主库 root'),
('db_instance', 1, 'dev_user', 'devPass@123', 'MySQL dev 开发用户'),
('db_instance', 4, 'root', 'prodMysqlRoot@1', '生产 MySQL root 用户');
