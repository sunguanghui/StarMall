# 星途补给站

> 面向家庭的星际主题亲子积分奖励系统。家长以「舰长」身份为孩子发放**星辰币**，孩子在**能量商城**兑换心仪奖励，通过**任务大厅**完成打卡赢取能量，通过**星际心愿单**表达心愿。支持多级管理员协同，可局域网或公网私有化部署。

---

## 预览

<img width="1780" height="919" alt="preview" src="https://github.com/user-attachments/assets/3f063f02-b84f-47c9-a7b3-69794388c98f" />

---

## 功能特性

### 积分机制
- **星辰币发放**：单星辰币（+1 能量）、双星辰币（+5 能量），对应不同程度的鼓励
- **阶梯式惩罚**：陨石撞击（-2）、星暴气流（-5）、黑洞吞噬（-10），支持自定义大额扣分；可用能量最低归零，不产生负债
- **大额惩罚视觉强化**：扣 5 分及以上记录显示 ☄️ 图标 + 深红加粗，移动端卡片变为红色背景
- **舰长寄语**：发放时可附加文字留言，在孩子流水记录中以提示条展示
- **赋能官审计**：每笔能量记录关联具体操作管理员，流水显示「赋能官 ✨」

### 任务大厅
- **每日日常**：每天可打卡一次，自动去重防重复提交
- **阶段里程碑**：无次数限制，适合长期目标
- 管理员创建任务时可指定**专属审批人**（仅超级管理员可设置），普通管理员只审批自己负责的任务
- 打卡审批后自动发放能量并写入流水记录

### 多级管理员
- **超级管理员（舰长）**：拥有全部权限，可管理用户、商品、兑换、心愿审核，可查看所有任务和打卡
- **普通管理员（领航员）**：只能发放星辰币、管理自己创建的任务、审批自己负责的打卡
- 前端菜单自动按权限隔离，后端 API 双重校验，越权操作返回 403

### 能量商城
- 商品列表浏览、关键词搜索、分页
- **盲盒商品**：特殊金色卡片样式，兑换时后端随机抽取预设奖池中的奖品
- 单次可兑换多件，系统自动校验积分和库存上限
- 兑换记录支持取消并退回积分与库存

### 星际心愿单
- 孩子提交心愿（名称 + 期望能量值）
- 管理员审核：批准后自动写入商品表（下架状态）；拒绝则标记关闭
- 心愿状态实时反馈：待审核 / 已批准 / 已拒绝

### 头像系统
- 6 款预设宇宙主题 emoji 头像（🚀 👨‍🚀 🌟 🪐 🛸 ⭐）
- 支持上传本地图片（jpg / png / gif / webp，限 5MB），存于服务器 `uploads/avatars/`
- 管理员可在用户管理中为任意用户设置头像

### 数据可视化
- 用户仪表板内置 **ECharts 折线图**，展示能量累计趋势
- 管理员仪表板展示全局统计：总用户数、星辰币发放总量、兑换总量、在架商品数
- 数据权限隔离：普通用户只见自己的流水，管理员只见自己操作的记录

### 用户与权限
- JWT 认证，Token 有效期 24 小时
- 三级角色：超级管理员 / 普通管理员 / 普通用户，前端路由守卫 + 后端 API 双重校验
- 支持自主注册、修改密码、管理员重置任意用户密码

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
users              用户表（超级管理员 / 普通管理员 / 普通用户，含头像字段）
thumbs_records     星辰币流水记录（含阶梯扣分、舰长寄语、赋能官审计字段）
products           商品表（含盲盒标识）
exchange_records   兑换记录（含盲盒抽奖结果）
wishlists          星际心愿单
tasks              任务模板（含专属审批人、创建者）
task_logs          任务打卡记录（含审批状态）
```

外键关系：
- `thumbs_records` / `exchange_records` / `wishlists` / `task_logs` → `users`
- `exchange_records` → `products`
- `task_logs` → `tasks`
- `tasks.reviewer_id` / `tasks.created_by` → `users`
- `thumbs_records.admin_id` / `thumbs_records.given_by` → `users`

---

## 目录结构

```
StarMall/
├── backend/
│   ├── app.py                   # 全部 API 路由
│   ├── models.py                # SQLAlchemy 数据模型（7 张表）
│   ├── config.py                # 配置类，读取 .env
│   ├── requirements.txt         # Python 依赖
│   ├── uploads/
│   │   └── avatars/             # 用户头像图片存储目录
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Dashboard.vue    # 仪表板（含 ECharts 图表）
│   │   │   ├── Mall.vue         # 能量商城（含盲盒）
│   │   │   ├── MyPoints.vue     # 我的能量流水（含大额惩罚视觉）
│   │   │   ├── MyExchanges.vue  # 兑换记录
│   │   │   ├── Wishlist.vue     # 星际心愿单（用户端）
│   │   │   ├── Tasks.vue        # 任务大厅（用户端）
│   │   │   ├── Help.vue         # 航行指南
│   │   │   ├── ChangePassword.vue
│   │   │   └── admin/
│   │   │       ├── Users.vue        # 用户管理（含头像、超级管理员设置）
│   │   │       ├── Thumbs.vue       # 发放星辰币（含阶梯惩罚面板）
│   │   │       ├── Products.vue
│   │   │       ├── Exchanges.vue
│   │   │       ├── Wishlists.vue    # 心愿审核
│   │   │       └── AdminTasks.vue   # 任务管理 + 打卡审核
│   │   ├── layouts/MainLayout.vue   # 含个人中心弹窗、权限菜单
│   │   ├── router/index.js          # 含 requireSuperAdmin 守卫
│   │   ├── stores/user.js           # 含 isSuperAdmin()
│   │   └── utils/api.js
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf
│   └── Dockerfile
├── database/
│   └── init.sql                 # 一次性建表 + 测试数据（7 张表全量）
└── docker-compose.yml
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
MYSQL_DATABASE=star_mall

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
| `starmall_db` | MySQL 8.0 数据库（Asia/Shanghai 时区） | 仅内部 3306 |
| `starmall_backend` | Flask + Gunicorn | **28001** |
| `starmall_frontend` | Nginx 静态托管 + 反向代理 | **28000** |

### 默认账号

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| `admin` | `admin123` | 超级管理员 | 拥有全部权限 |
| `zhangsan` | `user123` | 普通用户 | 初始 100 能量 |
| `lisi` | `user123` | 普通用户 | 初始 50 能量 |

> 新增普通管理员（领航员）账号：在用户管理中创建 `role=admin`、`is_super_admin=false` 的账号即可。

---

## API 概览

Base URL：`http://localhost:28001/api`

所有需要认证的接口需在请求头携带：`Authorization: Bearer <token>`

| 分类 | 方法 | 路径 | 权限 |
|------|------|------|------|
| **认证** | POST | `/auth/login` | — |
| | POST | `/auth/register` | — |
| | GET | `/auth/info` | ✓ |
| | POST | `/auth/change-password` | ✓ |
| | POST | `/auth/avatar` | ✓ |
| **用户** | GET | `/users` | ✓ 管理员 |
| | POST | `/users` | ✓ 管理员 |
| | PUT | `/users/{id}` | ✓ |
| | POST | `/users/{id}/reset-password` | ✓ 管理员 |
| | GET | `/admins` | ✓ 管理员 |
| **文件** | POST | `/upload/avatar` | ✓ |
| | GET | `/uploads/avatars/{filename}` | — |
| | POST | `/upload` | ✓ |
| | GET | `/uploads/{filename}` | — |
| **星辰币** | POST | `/thumbs` | ✓ 管理员 |
| | GET | `/thumbs` | ✓ |
| | GET | `/thumbs/stats` | ✓ |
| **商品** | GET | `/products` | — |
| | GET | `/products/{id}` | — |
| | POST | `/products` | ✓ 超级管理员 |
| | PUT | `/products/{id}` | ✓ 超级管理员 |
| | POST | `/products/{id}/toggle-status` | ✓ 超级管理员 |
| | DELETE | `/products/{id}` | ✓ 超级管理员 |
| **兑换** | POST | `/exchanges` | ✓ |
| | GET | `/exchanges` | ✓ |
| | POST | `/exchanges/{id}/cancel` | ✓ |
| **心愿单** | POST | `/wishlists` | ✓ |
| | GET | `/wishlists` | ✓ |
| | POST | `/wishlists/{id}/approve` | ✓ 超级管理员 |
| | POST | `/wishlists/{id}/reject` | ✓ 超级管理员 |
| **任务** | GET | `/tasks` | ✓ |
| | POST | `/tasks` | ✓ 管理员 |
| | PUT | `/tasks/{id}` | ✓ 管理员（限创建者）|
| | DELETE | `/tasks/{id}` | ✓ 管理员（限创建者）|
| **打卡** | POST | `/task-logs` | ✓ |
| | GET | `/task-logs` | ✓ |
| | POST | `/task-logs/{id}/approve` | ✓ 管理员 |
| | POST | `/task-logs/{id}/reject` | ✓ 管理员 |
| **统计** | GET | `/stats/dashboard` | ✓ |

---

## 常见问题

**Q：数据库连接失败**
检查 `backend/.env` 中的 `MYSQL_PASSWORD` 是否与 MySQL 实际密码一致，确认 MySQL 服务已启动。

**Q：登录时提示用户名或密码错误**
使用 `backend/reset_admin.py` 重置管理员密码。

**Q：商品图片 / 头像图片不显示**
确认后端服务正在运行，且 `backend/uploads/` 和 `backend/uploads/avatars/` 目录存在且有写权限（Docker 挂载卷自动创建）。

**Q：前端请求 API 报跨域错误**
后端已全局启用 CORS。若部署在不同域名，在 `backend/app.py` 的 `CORS(app)` 处添加 `origins` 参数指定允许的来源。

**Q：Docker 部署后界面空白**
确认前端 Vite 构建成功（`docker-compose logs frontend`），检查 `frontend/nginx.conf` 中 `proxy_pass` 指向的后端服务名是否为 `backend`。

**Q：普通管理员登录后看不到任务**
普通管理员只能看到自己创建的任务。需由超级管理员创建任务并将其指定为审批人，或普通管理员自行在任务管理中新建任务。

**Q：时间显示与实际不符**
`docker-compose.yml` 中所有服务已配置 `TZ: Asia/Shanghai`，MySQL 也已设置 `--default-time-zone='+08:00'`。如有问题请确认 Docker 宿主机时区设置。
