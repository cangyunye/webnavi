-- 状态字段迁移脚本: TINYINT → VARCHAR(20)
-- 将 dev_machines 和 db_instances 的 status 从 0/1 改为 online/offline/pending/error

ALTER TABLE dev_machines MODIFY COLUMN status VARCHAR(20) DEFAULT 'online';
UPDATE dev_machines SET status = 'online' WHERE status = '1';
UPDATE dev_machines SET status = 'offline' WHERE status = '0';

ALTER TABLE db_instances MODIFY COLUMN status VARCHAR(20) DEFAULT 'online';
UPDATE db_instances SET status = 'online' WHERE status = '1';
UPDATE db_instances SET status = 'offline' WHERE status = '0';

-- 补充示例数据
INSERT INTO dev_machines (name, ip, port, hostname, cpu, memory, disk, os, status, environment, description) VALUES
('故障服务器-01', '192.168.1.250', 22, 'failed-server-01', '8核 Intel Xeon', '16GB', '500GB SSD', 'Ubuntu 22.04 LTS', 'error', 'dev', '硬件故障，待修复'),
('待审批服务器-01', '192.168.1.251', 22, 'pending-server-01', '8核 Intel Xeon', '16GB', '500GB SSD', 'CentOS 9', 'pending', 'test', '新购服务器等待审批'),
('待审批服务器-02', '192.168.1.252', 22, 'pending-server-02', '16核 AMD EPYC', '32GB', '1TB SSD', 'Rocky Linux 9', 'pending', 'staging', '预发布环境等待上线'),
('离线服务器-01', '192.168.1.253', 22, 'offline-server-01', '8核 Intel Xeon', '16GB', '500GB HDD', 'CentOS 7', 'offline', 'dev', '已退役，待下架'),
('备用机器-01', '192.168.1.254', 22, 'spare-server-01', '16核 Intel Xeon', '32GB', '1TB SSD', 'Ubuntu 22.04 LTS', 'offline', 'prod', '备用机器，冷备状态');

INSERT INTO db_instances (name, db_type, version, ip, port, charset, status, environment, description) VALUES
('故障MySQL', 'MySQL', '8.0', '192.168.2.200', 3306, 'utf8mb4', 'error', 'dev', '数据库异常，IO 挂载失败'),
('待审批PG', 'PostgreSQL', '16', '192.168.2.201', 5432, 'UTF8', 'pending', 'test', '新部署待验收'),
('待审批Redis', 'Redis', '7.2', '192.168.2.202', 6379, 'UTF8', 'pending', 'staging', '缓存实例等待上线'),
('离线MySQL', 'MySQL', '8.0', '192.168.2.203', 3306, 'utf8mb4', 'offline', 'dev', '已废弃待清理'),
('备用Mongo', 'MongoDB', '7.0', '192.168.2.204', 27017, 'UTF8', 'offline', 'prod', '冷备数据库');
