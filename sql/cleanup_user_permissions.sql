-- 删除未使用的 user_permissions 表
-- 使用方法: mysql -u your_user -p your_database < sql/cleanup_user_permissions.sql

USE resource_nav;

-- 删除 user_permissions 表（如果有外键约束，先删除约束）
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS user_permissions;
SET FOREIGN_KEY_CHECKS = 1;

SELECT 'user_permissions 表已删除' AS result;
