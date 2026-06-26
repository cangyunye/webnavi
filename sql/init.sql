-- ResourceNav 数据库初始化
-- 用法: mycli -h 127.0.0.1 -uroot -proot123456 -e "SOURCE sql/init.sql"
--
-- 该脚本依次执行:
--   1. schema.sql — 创建所有表结构
--   2. seed.sql   — 写入示例数据

SOURCE schema.sql;
SOURCE seed.sql;
