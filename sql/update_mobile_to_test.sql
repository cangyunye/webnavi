-- 将数据库中现有的"移动通信"分类改为"测试"
-- 使用方法: mysql -u your_user -p your_database < sql/update_mobile_to_test.sql

USE resource_nav;

-- 更新分类表中的名称和图标
UPDATE categories 
SET name = '测试', icon = 'icon-test' 
WHERE name = '移动通信';

-- 更新枚举表中的相关数据（如果存在）
UPDATE enum_items 
SET enum_label = '测试' 
WHERE enum_type = 'category' AND enum_value = '移动通信';

-- 更新用户权限表中引用的分类名称（如果使用了名称而不是ID）
-- 注意：通常权限表应该使用category_id，这里留作参考
-- UPDATE user_permissions SET ... 

SELECT '更新完成' AS result;
