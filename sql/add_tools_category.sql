-- 添加"工具"分类
-- 创建时间: 2025

INSERT IGNORE INTO categories (name, icon, sort_order) VALUES ('工具', 'icon-tools', 8);

-- 添加示例资源
INSERT INTO resources (category_id, name, url, description, status)
SELECT id, 'wttr.in', 'https://wttr.in', '命令行风格的天气预报工具，支持 curl 直接调用', 1
FROM categories WHERE name = '工具'
AND NOT EXISTS (SELECT 1 FROM resources WHERE name = 'wttr.in');

INSERT INTO resources (category_id, name, url, description, status)
SELECT id, 'Public APIs', 'https://github.com/public-apis/public-apis', '开源 API 集合，收录各种免费 API 接口', 1
FROM categories WHERE name = '工具'
AND NOT EXISTS (SELECT 1 FROM resources WHERE name = 'Public APIs');

INSERT INTO resources (category_id, name, url, description, status)
SELECT id, 'Papers With Code', 'https://paperswithcode.com', '机器学习论文 + 数据集 + 代码实现汇总', 1
FROM categories WHERE name = '工具'
AND NOT EXISTS (SELECT 1 FROM resources WHERE name = 'Papers With Code');

INSERT INTO resources (category_id, name, url, description, status)
SELECT id, 'Hugging Face Datasets', 'https://huggingface.co/datasets', '开源机器学习数据集仓库', 1
FROM categories WHERE name = '工具'
AND NOT EXISTS (SELECT 1 FROM resources WHERE name = 'Hugging Face Datasets');

INSERT INTO resources (category_id, name, url, description, status)
SELECT id, 'DevDocs', 'https://devdocs.io', '开发者文档聚合查询工具', 1
FROM categories WHERE name = '工具'
AND NOT EXISTS (SELECT 1 FROM resources WHERE name = 'DevDocs');
