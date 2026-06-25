-- 补充测试和运维分类的示例资源

INSERT INTO resources (category_id, name, url, description, status)
SELECT 5, name, url, descr, 1 FROM (
  SELECT 'Postman' AS name, 'https://postman.com' AS url, 'API 测试与调试工具' AS descr
  UNION SELECT 'Selenium', 'https://selenium.dev', '浏览器自动化测试框架'
  UNION SELECT 'Jest', 'https://jestjs.io', 'JavaScript 测试框架'
  UNION SELECT 'JMeter', 'https://jmeter.apache.org', '性能测试与负载测试工具'
  UNION SELECT 'Swagger', 'https://swagger.io', 'API 文档与测试工具'
) t WHERE NOT EXISTS (SELECT 1 FROM resources r WHERE r.name = t.name AND r.category_id = 5);

INSERT INTO resources (category_id, name, url, description, status)
SELECT 7, name, url, descr, 1 FROM (
  SELECT 'Grafana' AS name, 'https://grafana.com' AS url, '监控与可视化平台' AS descr
  UNION SELECT 'Prometheus', 'https://prometheus.io', '系统监控与告警套件'
  UNION SELECT 'Jenkins', 'https://jenkins.io', 'CI/CD 持续集成平台'
  UNION SELECT 'Ansible', 'https://ansible.com', '配置管理与自动化工具'
  UNION SELECT 'ELK Stack', 'https://elastic.co', '日志采集与分析平台'
) t WHERE NOT EXISTS (SELECT 1 FROM resources r WHERE r.name = t.name AND r.category_id = 7);
