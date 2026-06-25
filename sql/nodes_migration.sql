-- CMDB 节点表迁移脚本
-- 创建时间: 2025

CREATE TABLE IF NOT EXISTS nodes (
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
