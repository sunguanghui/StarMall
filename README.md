# 星途补给站

> 面向家庭的星际主题亲子积分奖励系统。家长以「舰长」身份为孩子发放**星辰币**，孩子在**能量商城**兑换心仪奖励，通过**星际心愿单**表达心愿。系统支持局域网或公网私有化部署。

---

## 预览

<img width="1780" height="919" alt="preview" src="https://github.com/user-attachments/assets/3f063f02-b84f-47c9-a7b3-69794388c98f" />

---

## 功能特性

### 积分机制
- **星辰币发放**：单星辰币（+1 能量）、双星辰币（+5 能量），对应不同程度的鼓励
- **红牌警告**：支持扣除能量（-1），用于行为纠正
- **舰长寄语**：发放时可附加文字留言，在孩子流水记录中以提示条展示
- **能量流水**：完整记录每一笔变动，负数以红色高亮显示

### 能量商城
- 商品列表浏览、关键词搜索、分页
- **盲盒商品**：特殊金色卡片样式，兑换时后端随机抽取预设奖池中的奖品
- 单次可兑换多件，系统自动校验积分和库存上限
- 兑换记录支持取消并退回积分与库存

### 星际心愿单
- 孩子提交心愿（名称 + 期望能量值）
- 管理员审核：批准后自动写入商品表（下架状态），拒绝则标记关闭
- 心愿状态实时反馈：待审核 / 已批准 / 已拒绝

### 数据可视化
- 用户仪表板内置 **ECharts 折线图**，展示能量累计趋势
- 管理员仪表板展示全局统计：总用户数、星辰币发放总量、兑换总量、在架商品数

### 用户与权限
- JWT 认证，Token 有效期 24 小时
- 两级角色：`admin`（家长）/ `user`（孩子），前端路由守卫 + 后端 API 双重校验
- 支持自主注册、修改密码、管理员重置任意用户密码

### 商品管理
- 商品 CRUD、上架/下架一键切换
- 本地图片上传（支持 jpg / png / gif / webp，限 5MB）
- 盲盒开关、排序权重配置

---

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue | 3.4 |
| 构建工具 | Vite | 5.0 |
| UI 组件库 | Element Plus | 2.5 |
| 状态管理 | Pinia | 2.1 |
| 路由 | Vue Router | 4.2 |
| 图表 | ECharts | 6.1 |
| HTTP 客户端 | Axios | 1.6 |
| 后端框架 | Flask | 3.0 |
| ORM | Flask-SQLAlchemy | 3.1 |
| 认证 | Flask-JWT-Extended | 4.6 |
| 跨域 | Flask-CORS | 4.0 |
| 数据库 | MySQL | 8.0+ |

---

## 数据库结构

```
users              用户表（管理员 / 普通用户）
thumbs_records     星辰币流水记录（含扣分、舰长寄语）
products           商品表（含盲盒标识）
exchange_records   兑换记录（含盲盒抽奖结果）
wishlists          星际心愿单
```

外键关系：`thumbs_records` / `exchange_records` / `wishlists` → `users`；`exchange_records` → `products`

---

## 目录结构

```
StarMall/
├── backend/
│   ├── app.py                   # 全部 API 路由（认证、星辰币、商品、兑换、心愿单、统计）
│   ├── models.py                # SQLAlchemy 数据模型（5 张表）
│   ├── config.py                # 配置类，读取 .env
│   ├── requirements.txt         # Python 依赖
│   ├── run.bat                  # Windows 一键启动脚本
│   ├── reset_admin.py           # 管理员密码重置脚本
│   ├── reset_passwords_simple.py  # 批量重置测试账号密码
│   ├── uploads/                 # 商品图片存储目录
│   ├── Dockerfile
│   └── API.md                   # REST 接口完整文档
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Dashboard.vue    # 仪表板（含 ECharts 图表）
│   │   │   ├── Mall.vue         # 能量商城（含盲盒）
│   │   │   ├── MyPoints.vue     # 我的能量流水
│   │   │   ├── MyExchanges.vue  # 兑换记录
│   │   │   ├── Wishlist.vue     # 星际心愿单（用户端）
│   │   │   ├── ChangePassword.vue
│   │   │   └── admin/
│   │   │       ├── Users.vue
│   │   │       ├── Thumbs.vue   # 发放星辰币
│   │   │       ├── Products.vue
│   │   │       ├── Exchanges.vue
│   │   │       └── Wishlists.vue  # 心愿审核（管理员端）
│   │   ├── layouts/MainLayout.vue
│   │   ├── router/index.js
│   │   ├── stores/user.js
│   │   └── utils/api.js         # Axios 封装与拦截器
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf
│   └── Dockerfile
├── database/
│   └── init.sql                 # 一次性建表 + 测试数据（5 张表全量）
├── docker-compose.yml
├── docs/
│   ├── DEPLOY.md
│   ├── 项目架构说明.md
│   ├── 功能清单.md
│   └── ...
└── README.md
```

---

## 快速启动

### 环境要求

- Docker 20+
- Docker Compose 2.0+

### 步骤一：配置环境变量

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

将 `docker-compose.yml` 中的 `MYSQL_ROOT_PASSWORD` 改为与上方 `MYSQL_PASSWORD` 一致的值。

### 步骤二：一键启动

```bash
docker-compose up -d
```

首次启动会自动执行 `database/init.sql`，完成建表和测试数据写入。

访问地址：`http://localhost:28000`

> 生产环境建议在前置 Nginx 配置 HTTPS，并将密钥替换为足够随机的值。

### 服务说明

| 服务 | 说明 | 端口 |
|------|------|------|
| `starmall_db` | MySQL 8.0 数据库 | 仅内部 3306 |
| `starmall_backend` | Flask + Gunicorn | **28001** |
| `starmall_frontend` | Nginx 静态托管 + 反向代理 | **28000** |

### 默认账号

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| `admin` | `admin123` | 管理员 | 家长，拥有全部管理权限 |
| `zhangsan` | `user123` | 普通用户 | 孩子，初始 100 能量 |
| `lisi` | `user123` | 普通用户 | 孩子，初始 50 能量 |

---

## API 概览

Base URL：`http://localhost:28001/api`

所有需要认证的接口需在请求头携带：`Authorization: Bearer <token>`

| 分类 | 方法 | 路径 | 认证 |
|------|------|------|------|
| **认证** | POST | `/auth/login` | — |
| | POST | `/auth/register` | — |
| | GET | `/auth/info` | ✓ |
| | POST | `/auth/change-password` | ✓ |
| **用户** | GET | `/users` | ✓ |
| | POST | `/users` | ✓ 管理员 |
| | PUT | `/users/{id}` | ✓ |
| | POST | `/users/{id}/reset-password` | ✓ 管理员 |
| **星辰币** | POST | `/thumbs` | ✓ 管理员 |
| | GET | `/thumbs` | ✓ |
| | GET | `/thumbs/stats` | ✓ |
| **商品** | GET | `/products` | — |
| | GET | `/products/{id}` | — |
| | POST | `/products` | ✓ 管理员 |
| | PUT | `/products/{id}` | ✓ 管理员 |
| | POST | `/products/{id}/toggle-status` | ✓ 管理员 |
| | DELETE | `/products/{id}` | ✓ 管理员 |
| **兑换** | POST | `/exchanges` | ✓ |
| | GET | `/exchanges` | ✓ |
| | POST | `/exchanges/{id}/cancel` | ✓ |
| **心愿单** | POST | `/wishlists` | ✓ |
| | GET | `/wishlists` | ✓ |
| | POST | `/wishlists/{id}/approve` | ✓ 管理员 |
| | POST | `/wishlists/{id}/reject` | ✓ 管理员 |
| **统计** | GET | `/stats/dashboard` | ✓ |
| **文件** | POST | `/upload` | ✓ |
| | GET | `/uploads/{filename}` | — |

完整请求/响应示例见 [`backend/API.md`](backend/API.md)。

---

## 常见问题

**Q：数据库连接失败**  
检查 `backend/.env` 中的 `MYSQL_PASSWORD` 是否与 MySQL 实际密码一致，确认 MySQL 服务已启动。

**Q：登录时提示用户名或密码错误**  
使用 `backend/reset_admin.py` 重置管理员密码，或运行 `reset_passwords_simple.py` 批量重置所有测试账号。

**Q：商品图片不显示**  
确认后端服务正在运行（图片通过 `/api/uploads/` 接口提供），且 `backend/uploads/` 目录存在。

**Q：前端请求 API 报跨域错误**  
后端已全局启用 CORS。若部署在不同域名，在 `backend/app.py` 的 `CORS(app)` 处添加 `origins` 参数指定允许的来源。

**Q：Docker 部署后界面空白**  
确认前端 Vite 构建成功（`docker-compose logs frontend`），检查 `frontend/nginx.conf` 中 `proxy_pass` 指向的后端服务名是否为 `backend`。

---

## 参考文档

| 文档 | 说明 |
|------|------|
| [`backend/API.md`](backend/API.md) | REST 接口完整参考 |
| [`docs/DEPLOY.md`](docs/DEPLOY.md) | 生产环境部署、Nginx、HTTPS 配置 |
| [`docs/项目架构说明.md`](docs/项目架构说明.md) | 系统架构、业务流程、扩展建议 |
| [`docs/功能清单.md`](docs/功能清单.md) | 完整功能列表与技术指标 |
| [`docs/测试清单.md`](docs/测试清单.md) | 功能测试用例清单 |
