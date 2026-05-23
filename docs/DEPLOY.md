# 星途补给站 · 部署指南

## 环境要求

| 组件 | 版本要求 |
|------|---------|
| Docker | 20+ |
| Docker Compose | 2.0+ |

---

## 快速部署

### 1. 克隆项目

```bash
git clone <repo-url>
cd StarMall
```

### 2. 配置环境变量

```bash
cp backend/.env.bak backend/.env
```

编辑 `backend/.env`：

```ini
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_strong_password
MYSQL_DATABASE=thumbs_mall

# 生产环境务必替换为随机长字符串
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

### 3. 配置 docker-compose.yml

将 `MYSQL_ROOT_PASSWORD` 改为与 `.env` 中 `MYSQL_PASSWORD` 一致的值：

```yaml
environment:
  MYSQL_ROOT_PASSWORD: your_strong_password
  MYSQL_DATABASE: thumbs_mall
```

> `MYSQL_HOST` 在 Docker 环境中固定为 `db`（服务名），不能填 `localhost`。

### 4. 启动所有服务

```bash
docker-compose up -d
```

首次启动会自动执行 `database/init.sql`，完成建表和测试数据写入，无需手动初始化数据库。

访问地址：`http://服务器IP:28000`

---

## 服务说明

| 服务名 | 说明 | 对外端口 |
|--------|------|---------|
| `starmall_db` | MySQL 8.0 | 3306（仅内部） |
| `starmall_backend` | Flask + Gunicorn（2 workers） | 5000（仅内部） |
| `starmall_frontend` | Nginx 静态托管 + 反向代理 | **28000** |

---

## 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `admin123` | 管理员（舰长） |
| `zhangsan` | `user123` | 普通用户 |
| `lisi` | `user123` | 普通用户 |

---

## 常用管理命令

```bash
# 查看运行状态
docker-compose ps

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend

# 重启某个服务
docker-compose restart backend

# 停止所有服务
docker-compose down

# 停止并删除数据卷（会清除数据库，谨慎使用）
docker-compose down -v
```

---

## 重置密码

### 重置管理员密码

```bash
docker-compose exec backend python reset_admin.py
```

---

## 数据维护

### 备份数据库

```bash
docker-compose exec db mysqldump -u root -p thumbs_mall > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 恢复数据库

```bash
cat backup.sql | docker-compose exec -T db mysql -u root -p thumbs_mall
```

---

## 生产环境配置

### HTTPS（推荐 Nginx 反向代理）

在服务器前置一层 Nginx，将 443 流量代理到 `28000` 端口：

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:28000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

申请证书：

```bash
certbot --nginx -d your-domain.com
```

---

## 常见问题

**首次启动数据库初始化失败**

MySQL 容器首次启动较慢，backend 可能提前尝试连接而失败。等待约 30 秒后重启 backend：

```bash
docker-compose restart backend
```

**Token 失效或登录跳转异常**

清除浏览器 localStorage（`F12 → Application → Local Storage → 清除`），重新登录。

**图片上传成功但不显示**

确认 backend 容器正常运行，`/api/uploads/` 路由由 Flask 提供静态文件服务。

**前端界面空白**

查看前端构建日志：

```bash
docker-compose logs frontend
```

确认 `frontend/nginx.conf` 中 `proxy_pass` 指向的后端服务名为 `backend`。
