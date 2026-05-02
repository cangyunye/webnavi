# 部署指南

本文档详细介绍 ResourceNav 的部署步骤。

## 目录

- [环境要求](#环境要求)
- [本地开发部署](#本地开发部署)
- [Docker 部署](#docker-部署)
- [生产环境部署](#生产环境部署)
- [配置说明](#配置说明)
- [常见问题](#常见问题)

## 环境要求

- **操作系统**：Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python**：3.12+
- **MySQL**：8.0+
- **内存**：至少 2GB RAM
- **磁盘**：至少 1GB 可用空间

## 本地开发部署

### 1. 克隆项目

```bash
git clone <repository-url>
cd webnavi
```

### 2. 数据库配置

#### Windows

```bash
# 启动 MySQL 服务
net start MySQL80

# 导入数据库
mysql -u root -p < sql/init.sql
```

#### Linux/macOS

```bash
# 启动 MySQL
sudo systemctl start mysql

# 导入数据库
mysql -u root -p < sql/init.sql
```

### 3. 后端配置

```bash
cd backend

# 复制环境配置
cp .env.example .env

# 编辑 .env 文件，配置数据库连接
# MYSQL_HOST=localhost
# MYSQL_PORT=3306
# MYSQL_USER=root
# MYSQL_PASSWORD=your_password
# MYSQL_DATABASE=resource_nav
# SECRET_KEY=your_secret_key

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python main.py
```

### 4. 访问应用

打开浏览器访问 http://localhost:8000

## Docker 部署

### Docker Compose (推荐)

在项目根目录创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: resourcenav-db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: resource_nav
      TZ: Asia/Shanghai
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - resourcenav-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
    container_name: resourcenav-backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      MYSQL_HOST: db
      MYSQL_PORT: 3306
      MYSQL_USER: root
      MYSQL_PASSWORD: root_password
      MYSQL_DATABASE: resource_nav
      SECRET_KEY: your_production_secret_key_change_this
      APP_NAME: ResourceNav
      DEBUG: False
    depends_on:
      db:
        condition: service_healthy
    networks:
      - resourcenav-network
    volumes:
      - ./frontend:/app/frontend

volumes:
  mysql-data:

networks:
  resourcenav-network:
    driver: bridge
```

在 `backend/` 目录下创建 `Dockerfile`：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["python", "main.py"]
```

启动所有服务：

```bash
docker-compose up -d
```

查看日志：

```bash
docker-compose logs -f
```

停止服务：

```bash
docker-compose down
```

### 仅后端 Docker

构建镜像：

```bash
cd backend
docker build -t resourcenav-backend .
```

运行容器：

```bash
docker run -d \
  --name resourcenav-backend \
  -p 8000:8000 \
  -e MYSQL_HOST=localhost \
  -e MYSQL_PORT=3306 \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=your_password \
  -e MYSQL_DATABASE=resource_nav \
  -e SECRET_KEY=your_secret_key \
  -v $(pwd)/../frontend:/app/frontend \
  resourcenav-backend
```

## 生产环境部署

### 1. 系统准备 (Ubuntu)

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要工具
sudo apt install -y nginx git python3.12 python3-pip python3.12-venv

# 安装 MySQL 8.0
sudo apt install -y mysql-server

# 配置防火墙
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. 数据库配置

```bash
# 登录 MySQL
sudo mysql -u root -p

# 创建数据库和用户
CREATE DATABASE resource_nav CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'resourcenav'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON resource_nav.* TO 'resourcenav'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 导入数据
mysql -u resourcenav -p resource_nav < sql/init.sql
```

### 3. 应用部署

```bash
# 创建应用目录
sudo mkdir -p /var/www/resourcenav
cd /var/www/resourcenav

# 克隆代码
git clone <repository-url> .

# 创建虚拟环境
python3.12 -m venv venv
source venv/bin/activate

# 安装依赖
cd backend
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env
# 修改配置：
# MYSQL_USER=resourcenav
# MYSQL_PASSWORD=your_strong_password
# DEBUG=False
# SECRET_KEY=your_very_long_strong_secret_key
```

### 4. 使用 Gunicorn 和 Uvicorn

创建 `gunicorn_config.py`：

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "info"
accesslog = "/var/log/resourcenav/access.log"
errorlog = "/var/log/resourcenav/error.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
```

创建日志目录：

```bash
sudo mkdir -p /var/log/resourcenav
sudo chown -R $USER:$USER /var/log/resourcenav
```

### 5. Systemd 服务

创建 `/etc/systemd/system/resourcenav.service`：

```ini
[Unit]
Description=ResourceNav - 资源导航网站
After=network.target mysql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/resourcenav/backend
Environment="PATH=/var/www/resourcenav/venv/bin"
ExecStart=/var/www/resourcenav/venv/bin/gunicorn main:app -c gunicorn_config.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable resourcenav
sudo systemctl start resourcenav
sudo systemctl status resourcenav
```

### 6. Nginx 配置

创建 `/etc/nginx/sites-available/resourcenav`：

```nginx
upstream resourcenav_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 50M;

    access_log /var/log/nginx/resourcenav-access.log;
    error_log /var/log/nginx/resourcenav-error.log;

    # 前端静态文件
    location /frontend/ {
        alias /var/www/resourcenav/frontend/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API 代理
    location /api/ {
        proxy_pass http://resourcenav_backend/api/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 根路径重定向
    location = / {
        return 302 /frontend/index.html;
    }

    # FastAPI 文档
    location /docs {
        proxy_pass http://resourcenav_backend/docs;
        proxy_set_header Host $http_host;
    }

    location /openapi.json {
        proxy_pass http://resourcenav_backend/openapi.json;
        proxy_set_header Host $http_host;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/resourcenav /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL 配置 (Let's Encrypt)

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

Certbot 会自动配置 SSL。

### 8. 安全加固

```bash
# 修改目录权限
sudo chown -R www-data:www-data /var/www/resourcenav
sudo chmod -R 755 /var/www/resourcenav

# 配置 .env 权限
chmod 600 /var/www/resourcenav/backend/.env
```

## 配置说明

### .env 配置文件

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| APP_NAME | 应用名称 | ResourceNav API |
| DEBUG | 调试模式 | True |
| MYSQL_HOST | MySQL 主机 | localhost |
| MYSQL_PORT | MySQL 端口 | 3306 |
| MYSQL_USER | MySQL 用户 | root |
| MYSQL_PASSWORD | MySQL 密码 | - |
| MYSQL_DATABASE | 数据库名 | resource_nav |
| SECRET_KEY | JWT 密钥 | 必须修改 |
| ALGORITHM | JWT 算法 | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token 过期分钟 | 10080 (7天) |

### 生产环境建议配置

```env
DEBUG=False
ACCESS_TOKEN_EXPIRE_MINUTES=43200  # 30天
# 使用强密钥，如 openssl rand -hex 32
SECRET_KEY=your_very_strong_random_secret_key_here
```

## 备份与恢复

### 数据库备份

```bash
# 备份
mysqldump -u root -p resource_nav > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复
mysql -u root -p resource_nav < backup_20250502_120000.sql
```

### 定时备份脚本

创建 `/usr/local/bin/backup_resourcenav.sh`：

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/resourcenav"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
mysqldump -u resourcenav -p'your_password' resource_nav | gzip > $BACKUP_DIR/backup_$DATE.sql.gz
find $BACKUP_DIR -name 'backup_*.sql.gz' -mtime +30 -delete
```

添加到 Crontab：

```bash
sudo crontab -e
# 每天凌晨 2 点备份
0 2 * * * /usr/local/bin/backup_resourcenav.sh
```

## 监控与日志

### 应用日志

- Gunicorn 访问日志：`/var/log/resourcenav/access.log`
- Gunicorn 错误日志：`/var/log/resourcenav/error.log`
- Nginx 访问日志：`/var/log/nginx/resourcenav-access.log`
- Nginx 错误日志：`/var/log/nginx/resourcenav-error.log`

### 查看服务状态

```bash
# 查看应用服务
sudo systemctl status resourcenav
sudo journalctl -u resourcenav -f

# 查看 Nginx
sudo systemctl status nginx
sudo nginx -t

# 查看 MySQL
sudo systemctl status mysql
```

## 更新部署

```bash
cd /var/www/resourcenav

# 拉取最新代码
git pull

# 激活虚拟环境
source venv/bin/activate
cd backend

# 安装新依赖
pip install -r requirements.txt

# 执行数据库迁移（如有）
# mysql -u resourcenav -p resource_nav < migrations/xxx.sql

# 重启服务
sudo systemctl restart resourcenav
```

## 常见问题

### 502 Bad Gateway

检查：
1. 后端服务是否运行：`sudo systemctl status resourcenav`
2. Gunicorn 日志是否有错误
3. Nginx 配置是否正确：`sudo nginx -t`

### 数据库连接失败

检查：
1. MySQL 服务是否启动
2. .env 配置是否正确
3. 用户权限是否足够

### 静态资源 404

检查：
1. Nginx 配置中的 alias 路径是否正确
2. 目录权限是否正确

### 性能优化建议

1. 启用 Gzip 压缩（Nginx）
2. 配置 CDN 加速静态资源
3. 使用 Redis 缓存
4. 定期优化数据库
5. 配置负载均衡（高可用）
