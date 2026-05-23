# 星途补给站 · 部署指南

## 环境要求

| 组件 | 版本要求 |
|------|---------|
| Python | 3.8+ |
| Node.js | 16+ |
| MySQL | 8.0+ |
| Docker（可选） | 20+ |

---

## 方式一：本地手动部署

### 1. 初始化数据库

安装并启动 MySQL，然后执行初始化脚本（建表 + 测试数据一步完成）：

```bash
mysql -u root -p < database/init.sql
```

验证结果：

```sql
USE thumbs_mall;
SHOW TABLES;
```

应看到以下 5 张表：

```
exchange_records
products
thumbs_records
users
wishlists
```

### 2. 配置并启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 安装依赖
pip install -r requirements.txt

# 如网络较慢，可使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

复制环境变量文件并编辑：

```bash
cp .env.bak .env
```

`.env` 配置说明：

```ini
# 数据库连接
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password        # 改为实际密码
MYSQL_DATABASE=thumbs_mall

# 安全密钥（生产环境务必替换为随机字符串）
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

启动服务（默认监听 `0.0.0.0:5000`）：

```bash
python app.py
# Windows 也可双击 run.bat
```

### 3. 启动前端

```bash
cd frontend
npm install

# 如网络较慢，可使用淘宝镜像
npm install --registry=https://registry.npmmirror.com

npm run dev    # 开发服务器，默认端口 5173
```

浏览器访问 `http://localhost:5173`

### 4. 默认账号

| 用户名 | 密码 | 角色 | 初始能量 |
|--------|------|------|---------|
| `admin` | `admin123` | 管理员（舰长） | 0 |
| `zhangsan` | `user123` | 普通用户 | 100 |
| `lisi` | `user123` | 普通用户 | 50 |

---

## 方式二：Docker 部署（推荐生产使用）

### 1. 修改配置

编辑 `docker-compose.yml`，将 `MYSQL_ROOT_PASSWORD` 改为实际密码：

```yaml
environment:
  MYSQL_ROOT_PASSWORD: your_strong_password
  MYSQL_DATABASE: thumbs_mall
```

编辑 `backend/.env`，确保 `MYSQL_PASSWORD` 与上方一致：

```ini
MYSQL_HOST=db
MYSQL_PASSWORD=your_strong_password
```

> `MYSQL_HOST` 在 Docker 环境中固定填写 `db`（服务名），不是 `localhost`。

### 2. 启动所有服务

```bash
docker-compose up -d
```

首次启动会自动执行 `database/init.sql`，无需手动初始化数据库。

### 3. 服务说明

| 服务名 | 说明 | 对外端口 |
|--------|------|---------|
| `numbmall_db` | MySQL 8.0 | 3306 |
| `numbmall_backend` | Flask + Gunicorn（2 workers） | 仅内部 5000 |
| `numbmall_frontend` | Nginx 静态托管 + 反向代理 | **28000** |

访问地址：`http://服务器IP:28000`

### 4. 常用管理命令

```bash
# 查看运行状态
docker-compose ps

# 查看后端日志
docker-compose logs -f backend

# 重启某个服务
docker-compose restart backend

# 停止所有服务
docker-compose down

# 停止并删除数据卷（会清除数据库数据，谨慎使用）
docker-compose down -v
```

---

## 生产环境配置

### Nginx 反向代理（手动部署时）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 上传图片代理（与 API 同源）
    location /api/uploads/ {
        proxy_pass http://127.0.0.1:5000/api/uploads/;
    }
}
```

### systemd 服务（Linux 后台运行）

创建 `/etc/systemd/system/stargate.service`：

```ini
[Unit]
Description=StarGate Backend
After=network.target mysql.service

[Service]
User=www-data
WorkingDirectory=/path/to/backend
EnvironmentFile=/path/to/backend/.env
ExecStart=/path/to/venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable stargate
systemctl start stargate
```

### 前端生产构建

```bash
cd frontend
npm run build
# 产物在 frontend/dist/，部署到 Nginx 的 root 目录
```

### HTTPS 配置（Certbot）

```bash
certbot --nginx -d your-domain.com
```

---

## 数据维护

### 数据库备份

```bash
mysqldump -u root -p thumbs_mall > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 数据库恢复

```bash
mysql -u root -p thumbs_mall < backup_20260101_120000.sql
```

### 重置管理员密码

```bash
cd backend
python reset_admin.py
```

### 批量重置测试账号密码

```bash
cd backend
python reset_passwords_simple.py
```

---

## 常见问题

**数据库连接失败（`Can't connect to MySQL server`）**

- 确认 MySQL 服务已启动
- 检查 `.env` 中 `MYSQL_HOST`、`MYSQL_PORT`、`MYSQL_PASSWORD` 是否正确
- Docker 环境中 `MYSQL_HOST` 应填 `db`，不是 `localhost`

**前端请求 API 报 CORS 错误**

后端已全局启用 CORS。若自定义域名部署，在 `backend/app.py` 的 `CORS(app)` 处指定 `origins` 参数。

**Token 失效或登录跳转异常**

- 清除浏览器 localStorage（`F12 → Application → Local Storage → 清除`）
- 检查服务器系统时间是否准确

**图片上传成功但不显示**

图片通过后端接口 `/api/uploads/<filename>` 提供。确认后端服务正在运行，且 `backend/uploads/` 目录存在并有写入权限。

**npm install 失败或超时**

```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --registry=https://registry.npmmirror.com
```

**Docker 首次启动数据库初始化失败**

MySQL 容器首次启动较慢，backend 可能提前尝试连接而失败。等待约 30 秒后重启 backend：

```bash
docker-compose restart backend
```
