# 星途补给站

> 面向家庭的星际主题亲子积分奖励系统。家长以「舰长」身份为孩子发放**星辰币**，孩子在**能量商城**兑换心仪奖励，通过**任务大厅**完成打卡赢取能量，收集飞船碎片升级飞船，通过**星际心愿单**表达心愿。支持多级管理员协同，可局域网或公网私有化部署。

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
- **后悔药**：管理员发放后 15 分钟内可一键撤销，能量原子性回滚

### 飞船碎片 & 连击系统
- **碎片掉落**：每次打卡审批通过时 30% 概率随机掉落引擎🔧 / 雷达📡 / 船体🛡️ 碎片
- **飞船升级**：集齐三种碎片各 1 枚即可在首页升级飞船，等级驱动驾驶舱图标升阶
- **连击奖励**：连续每天完成任务，满 7 天触发「星云爆发」自动额外奖励 +10 能量
- **能量衰减**：连续 3 天无任务通过则每日自动扣除 1 点，保持活跃即可避免

### 任务大厅
- **每日日常**：每天可打卡一次，自动去重防重复提交
- **阶段里程碑**：无次数限制，适合长期目标
- 管理员创建任务时可指定**专属审批人**（仅超级管理员可设置），普通管理员只审批自己负责的任务
- 打卡审批后自动发放能量、触发碎片掉落检查、更新连击天数，并写入流水记录

### 多级管理员
- **超级管理员（舰长）**：拥有全部权限，可管理用户、商品、兑换、心愿审核，可查看所有任务和打卡
- **普通管理员（领航员）**：只能发放星辰币、管理自己创建的任务、审批自己负责的打卡
- 前端菜单自动按权限隔离，后端 API 双重校验，越权操作返回 403

### 管理员仪表板
- **待办雷达**：实时显示待核验任务数、待交付补给数、待解析蓝图数，点击直跳对应处理页
- **舰队成员概览**：展示所有宇航员能量状态，支持一键快速赋能
- **全站动态时间轴**：展示最近 15 条能量流水动态

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

### 自动化运维
- **定时数据库备份**：每日凌晨 3:00 自动 `mysqldump` 备份到 `backend/backups/`，保留最近 7 份
- **能量衰减定时任务**：每日 00:05 自动检查并执行非活跃用户能量衰减
- **定时星际简报**：由广播台配置驱动，每日在指定时间向音箱推送早晚简报，可动态修改时间无需重启服务

### 星际广播台
- **局域网音箱接入**：通过 WebSocket 连接支持 `ws://<IP>:<端口>/ws/status` 协议的音箱设备（端口默认 18888）
- **即时发分播报**：管理员发放正能量时，自动向音箱推送随机拼接的语音播报文案，包含宇航员姓名、获奖原因、能量变化及当前总能量
- **定时早晚简报**：APScheduler 驱动，可独立设置早晚时间；播报内容包含当前能量和最近待实现心愿的剩余差值追踪
- **播报目标配置**：可指定特定宇航员播报，留空则向全体宇航员播报
- **连接管理**：WebSocket 常驻后台线程，断线自动重连（指数退避，最长 60 秒），心跳间隔可配置
- **超级管理员专属**：配置页面与全部 API 均需 `is_super_admin=true`，支持一键发送测试广播验证连接

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
| 定时任务 | APScheduler | 3.10 |
| 数据库 | MySQL | 8.0+ |

---

## 系统架构

```
┌──────────────────────────────────────────────────────────────────┐
│                           用户浏览器                               │
│                    http://localhost:28000                          │
└─────────────────────────┬────────────────────────────────────────┘
                          │ HTTP
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Vue 3 前端（Vite + Nginx）                      │
│  ┌─────────────────┬─────────────────┬──────────────────────┐   │
│  │    公共页面       │    用户页面       │     管理员页面         │   │
│  │  Login          │  UserDashboard  │  AdminDashboard       │   │
│  │  Register       │  Mall           │  Users（仅舰长）       │   │
│  │                 │  MyPoints       │  Thumbs（发放）        │   │
│  │                 │  MyExchanges    │  Products（仅舰长）    │   │
│  │                 │  Wishlist       │  Exchanges（仅舰长）   │   │
│  │                 │  Tasks          │  TaskApproval         │   │
│  │                 │  Help           │  WishlistApproval     │   │
│  │                 │  ChangePassword │  AdminTasks           │   │
│  │                 │                 │  BroadcastSettings    │   │
│  └─────────────────┴─────────────────┴──────────────────────┘   │
│  状态管理：Pinia（user store）                                     │
│  路由守卫：requireAdmin · requireSuperAdmin                       │
└─────────────────────────┬────────────────────────────────────────┘
                          │ AJAX /api/*（含 JWT Bearer Token）
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Flask 后端 API + APScheduler                    │
│  认证 · 用户 · 文件 · 星辰币 · 商品 · 兑换 · 心愿单 · 任务 · 统计  │
│  系统设置 · 星际广播台（WebSocket 音箱客户端）                      │
│  定时任务：能量衰减（00:05）· 数据库备份（03:00）· 早晚简报（可配置）│
└─────────────────────────┬────────────────────────────────────────┘
                          │ SQLAlchemy ORM
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                      MySQL 8.0                                    │
│  users · thumbs_records · products · exchange_records            │
│  wishlists · tasks · task_logs · system_settings                 │
└──────────────────────────────────────────────────────────────────┘
```

### 角色权限说明

| 角色 | 称号 | 标识 | 权限范围 |
|------|------|------|---------|
| 超级管理员 | 👑 舰长 | `role=admin, is_super_admin=1` | 全部功能 |
| 普通管理员 | 领航员 | `role=admin, is_super_admin=0` | 发放星辰币、管理自己的任务、审批自己负责的打卡 |
| 普通用户 | 🚀 飞行员 | `role=user` | 浏览商城、兑换、打卡、心愿单 |

---

## 数据库结构

```
users              用户表（角色、头像、fragments 碎片、ship_level 飞船等级、streak_days 连击天数）
thumbs_records     星辰币流水记录（含阶梯扣分、舰长寄语、赋能官审计、is_deleted 软删除字段）
products           商品表（含盲盒标识）
exchange_records   兑换记录（含盲盒抽奖结果）
wishlists          星际心愿单
tasks              任务模板（含专属审批人、创建者）
task_logs          任务打卡记录（含审批状态）
system_settings    系统设置（音箱 IP、端口、播报开关、早晚时间、播报目标）
```

外键关系：
- `thumbs_records` / `exchange_records` / `wishlists` / `task_logs` → `users`
- `exchange_records` → `products`
- `task_logs` → `tasks`
- `tasks.reviewer_id` / `tasks.created_by` → `users`
- `thumbs_records.admin_id` / `thumbs_records.given_by` → `users`

### 关键字段说明

**thumbs_records.thumb_type**

| 值 | 含义 | points 变化 |
|----|------|------------|
| `single` | 单星辰币 ⭐ | +1 |
| `double` | 双星辰币 🚀 | +5 |
| `deduction` | 阶梯扣除 | 由 `points` 字段决定（负整数） |

> 扣除时 `available_points = max(0, available_points + points)`，不产生负债。

**tasks.type**

| 值 | 含义 | 打卡限制 |
|----|------|---------|
| `daily` | 每日日常 | 同一用户同一任务当天仅可打卡1次 |
| `milestone` | 阶段里程碑 | 无次数限制 |

**tasks.reviewer_id**：`NULL` = 所有管理员均可审批；非 NULL = 仅指定管理员可审批。

---

## 目录结构

```
StarMall/
├── backend/
│   ├── app.py                   # 全部 API 路由 + APScheduler 定时任务
│   ├── models.py                # SQLAlchemy 数据模型（8 张表）
│   ├── config.py                # 配置类，读取 .env
│   ├── speaker_client.py        # WebSocket 音箱客户端（单例、断线重连）
│   ├── requirements.txt         # Python 依赖
│   ├── reset_admin.py           # 管理员密码重置脚本
│   ├── uploads/
│   │   └── avatars/             # 用户头像图片存储目录
│   ├── backups/                 # 自动数据库备份目录（保留最近7份）
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Dashboard.vue        # 路由分发：管理员→AdminDashboard，用户→UserDashboard
│   │   │   ├── UserDashboard.vue    # 用户仪表板（含飞船碎片、连击展示、ECharts）
│   │   │   ├── Mall.vue             # 能量商城（含盲盒）
│   │   │   ├── MyPoints.vue         # 我的能量流水（含大额惩罚视觉）
│   │   │   ├── MyExchanges.vue      # 兑换记录
│   │   │   ├── Wishlist.vue         # 星际心愿单（用户端）
│   │   │   ├── Tasks.vue            # 任务大厅（用户端）
│   │   │   ├── Help.vue             # 星际航行指南
│   │   │   ├── ChangePassword.vue
│   │   │   └── admin/
│   │   │       ├── AdminDashboard.vue   # 管理员仪表板（待办雷达、舰队概览、全站动态）
│   │   │       ├── Users.vue            # 用户管理（含头像、超级管理员设置）
│   │   │       ├── Thumbs.vue           # 发放星辰币（含阶梯惩罚面板、后悔药）
│   │   │       ├── Products.vue         # 商品管理
│   │   │       ├── Exchanges.vue        # 兑换管理
│   │   │       ├── TaskApproval.vue     # 任务核验舱（打卡审批）
│   │   │       ├── ExchangeDelivery.vue # 补给调度室（兑换交付）
│   │   │       ├── WishlistApproval.vue # 蓝图解析室（心愿审核）
│   │   │       └── AdminTasks.vue       # 任务定义管理
│   │   ├── layouts/MainLayout.vue       # 含个人中心弹窗、角色隔离菜单
│   │   ├── router/index.js              # 含 requireAdmin / requireSuperAdmin 守卫
│   │   ├── stores/user.js               # 含 isAdmin() / isSuperAdmin()
│   │   └── utils/api.js
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf
│   └── Dockerfile
├── database/
│   └── init.sql                 # 一次性建表 + 测试数据（8 张表全量，含新增字段）
└── docker-compose.yml
```

---

## 快速部署

### 环境要求

| 组件 | 版本要求 |
|------|---------|
| Docker | 20+ |
| Docker Compose | 2.0+ |

### 步骤一：克隆项目并配置环境变量

```bash
git clone <repo-url>
cd StarMall
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

### 步骤二：同步 docker-compose.yml 密码

将 `docker-compose.yml` 中的 `MYSQL_ROOT_PASSWORD` 改为与 `.env` 中 `MYSQL_PASSWORD` 一致的值：

```yaml
environment:
  MYSQL_ROOT_PASSWORD: your_strong_password
  MYSQL_DATABASE: star_mall
```

> `MYSQL_HOST` 在 Docker 环境中固定为 `db`（服务名），不能填 `localhost`。

### 步骤三：一键启动

```bash
docker-compose up -d
```

首次启动会自动执行 `database/init.sql`，完成建表和测试数据写入，无需手动初始化数据库。

访问地址：`http://服务器IP:28000`

### 服务说明

| 服务 | 说明 | 端口 |
|------|------|------|
| `starmall_db` | MySQL 8.0 数据库（Asia/Shanghai 时区） | 仅内部 3306 |
| `starmall_backend` | Flask + Gunicorn + APScheduler | **28001** |
| `starmall_frontend` | Nginx 静态托管 + 反向代理 | **28000** |

### 默认账号

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| `admin` | `admin123` | 超级管理员（舰长） | 拥有全部权限 |
| `zhangsan` | `user123` | 普通用户 | 初始 100 能量 |
| `lisi` | `user123` | 普通用户 | 初始 50 能量 |

> **新增普通管理员（领航员）**：在用户管理中创建 `role=admin`、`is_super_admin=false` 的账号即可。  
> **新增超级管理员**：创建管理员账号时勾选「超级管理员」开关（需以舰长身份登录操作）。

---

## 环境变量说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `MYSQL_HOST` | MySQL 服务器地址（Docker 中固定为 `db`） | `db` |
| `MYSQL_PORT` | MySQL 端口 | `3306` |
| `MYSQL_USER` | MySQL 用户名 | `root` |
| `MYSQL_PASSWORD` | MySQL 密码 | 必填 |
| `MYSQL_DATABASE` | 数据库名称 | `star_mall` |
| `SECRET_KEY` | Flask 密钥 | 建议修改 |
| `JWT_SECRET_KEY` | JWT 密钥 | 建议修改 |

> `.env` 文件已在 `.gitignore` 中忽略，不会被提交到版本库。生产环境务必将 `SECRET_KEY` 和 `JWT_SECRET_KEY` 替换为足够随机的长字符串。

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

# 重置管理员密码
docker-compose exec backend python reset_admin.py

# 停止所有服务
docker-compose down

# 停止并删除数据卷（会清除数据库，谨慎使用）
docker-compose down -v
```

### 数据库手动备份与恢复

```bash
# 手动备份
docker-compose exec db mysqldump -u root -p star_mall > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
cat backup.sql | docker-compose exec -T db mysql -u root -p star_mall
```

自动备份文件存放在 `backend/backups/` 目录（容器内 `/app/backups/`），格式为 `YYYY-MM-DD.sql`，自动保留最近 7 份。

---

## 生产环境 HTTPS 配置

推荐在前置 Nginx 配置 HTTPS 并反向代理到 28000 端口：

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

## API 参考

Base URL：`http://localhost:28001/api`

所有需要认证的接口需在请求头携带：`Authorization: Bearer <token>`

### 权限速查

| 接口 | 普通用户 | 普通管理员 | 超级管理员 |
|------|---------|-----------|-----------|
| 发放星辰币 | ✗ | ✓ | ✓ |
| 用户管理 | ✗ | ✗ | ✓ |
| 商品管理（写） | ✗ | ✗ | ✓ |
| 兑换取消 | ✗ | ✗ | ✓ |
| 心愿审核 | ✗ | ✗ | ✓ |
| 任务创建/编辑 | ✗ | ✓（仅自己） | ✓ |
| 打卡审批 | ✗ | ✓（仅负责的） | ✓ |
| 设置审批人 | ✗ | ✗ | ✓ |
| 系统设置/广播台 | ✗ | ✗ | ✓ |

### 接口列表

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
| | POST | `/users/{id}/upgrade-ship` | ✓ 本人 |
| | GET | `/admins` | ✓ 管理员 |
| **文件** | POST | `/upload/avatar` | ✓ |
| | GET | `/uploads/avatars/{filename}` | — |
| | POST | `/upload` | ✓ |
| | GET | `/uploads/{filename}` | — |
| **星辰币** | POST | `/thumbs` | ✓ 管理员 |
| | GET | `/thumbs` | ✓ |
| | GET | `/thumbs/stats` | ✓ |
| | POST | `/thumbs/{id}/undo` | ✓ 管理员（15分钟内）|
| **商品** | GET | `/products` | — |
| | GET | `/products/{id}` | — |
| | POST | `/products` | ✓ 超级管理员 |
| | PUT | `/products/{id}` | ✓ 超级管理员 |
| | POST | `/products/{id}/toggle-status` | ✓ 超级管理员 |
| | DELETE | `/products/{id}` | ✓ 超级管理员 |
| **兑换** | POST | `/exchanges` | ✓ |
| | GET | `/exchanges` | ✓ |
| | POST | `/exchanges/{id}/complete` | ✓ 管理员 |
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
| **系统设置** | GET | `/settings` | ✓ 超级管理员 |
| | PUT | `/settings` | ✓ 超级管理员 |
| | POST | `/settings/test-broadcast` | ✓ 超级管理员 |

### 响应格式

```json
{
  "code": 200,
  "message": "成功",
  "data": {}
}
```

### 认证接口示例

**POST /auth/login**

```json
// 请求
{ "username": "admin", "password": "admin123" }

// 响应
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": { "id": 1, "username": "admin", "role": "admin", "is_super_admin": true }
  }
}
```

### 星辰币接口示例

**POST /thumbs** — 发放/扣除星辰币

```json
// 发放
{ "user_id": 2, "thumb_type": "single", "reason": "积极参与", "parent_message": "舰长寄语（选填）" }

// 阶梯扣除
{ "user_id": 2, "thumb_type": "deduction", "points": -5, "reason": "未完成任务" }
```

| `thumb_type` | 说明 | `points` |
|---|---|---|
| `single` | 单星辰币 | +1（固定） |
| `double` | 双星辰币 | +5（固定） |
| `deduction` | 阶梯扣除 | 由 `points` 字段指定（负整数） |

**GET /thumbs/stats** — 统计数据响应（普通用户）

```json
{
  "data": {
    "total_points": 100, "available_points": 80, "used_points": 20,
    "single_thumbs": 50, "double_thumbs": 25, "total_thumbs": 75
  }
}
```

### 任务接口示例

**POST /tasks** — 创建任务

```json
{
  "title": "完成今日阅读打卡",
  "type": "daily",
  "energy_reward": 1,
  "is_active": true,
  "reviewer_id": null
}
```

`type` 可为 `daily`（每日日常）或 `milestone`（阶段里程碑）。`reviewer_id` 为 `null` 表示所有管理员均可审批，仅超级管理员可设置非 null 值。

**GET /task-logs** 权限说明：普通用户只返回自己的记录；普通管理员返回自己负责审批的记录；超级管理员返回全部。

---

## 用户操作手册

### 账号管理

**注册**

| 字段 | 必填 | 要求 |
|------|------|------|
| 用户名 | ✓ | 3～20 个字符，不可重复 |
| 密码 | ✓ | 至少 6 位 |
| 确认密码 | ✓ | 需与密码一致 |
| 真实姓名 | ✓ | 用于显示和记录 |
| 邮箱 | — | 格式需正确 |
| 手机号 | — | — |

**修改密码**：点击右上角头像 → 修改密码，输入当前密码和新密码（至少6位）。修改成功后自动登出，需用新密码重新登录。

**头像设置**：点击右上角头像 → 个人中心，可选择预设 emoji（🚀 👨‍🚀 🌟 🪐 🛸 ⭐）或上传本地图片（jpg/png/gif/webp，≤5MB）。

### 首页仪表盘

| 卡片 | 说明 |
|------|------|
| 总能量 | 历史累计获得，只增不减 |
| 可用能量 | 当前可用于兑换的余额 |
| 获得星辰币 | 收到的星辰币记录总条数 |
| 兑换次数 | 已完成兑换的总次数 |

底部「飞船改造舱」展示飞船等级、碎片收集进度和连击天数；趋势图展示近期累计能量增长曲线。

### 飞船碎片 & 连击

每次管理员审批通过打卡时，系统有 **30% 概率**随机掉落引擎🔧 / 雷达📡 / 船体🛡️ 碎片。集齐三种各1枚后，在首页「飞船改造舱」点击「立即升级飞船」，消耗各1枚，飞船等级+1。

| 情况 | 效果 |
|------|------|
| 今日首次打卡被审批通过 | 连击天数 +1，更新最后活跃日期 |
| 同一天多次打卡通过 | 连击天数不重复累加 |
| 中断超过1天 | 连击天数重置为1 |
| 累计满7天（7、14、21…） | 触发「星云爆发」额外奖励 +10 能量 |

连续 **3 天**未完成任务（无审批通过记录），系统每日凌晨自动扣除 1 点能量。保持活跃即可避免。

### 能量商城

兑换限制说明：

| 条件 | 结果 |
|------|------|
| 库存为 0 | 按钮显示「已售罄」，不可点击 |
| 可用能量不足 | 按钮置灰，不可点击 |
| 能量或库存只够部分 | 兑换数量上限自动调整为最大可兑换件数 |

盲盒兑换成功后，在「兑换记录」页面的「备注」列可查看抽中的具体奖品。

### 我的能量（流水记录）

| 列名 | 说明 |
|------|------|
| 类型 | 单星辰币 / 双星辰币 / 扣除 |
| 能量 | 正数为获得，负数（红色）为扣除 |
| 原因 | 管理员备注的具体原因 |
| 舰长寄语 | 附加鼓励语（显示为蓝色提示条） |
| 赋能官 ✨ | 操作的管理员名称 |
| 时间 | 记录创建时间 |

> 扣除 5 分及以上的记录显示 ☄️ 图标并以深红加粗标注；移动端卡片变为红色背景。

### 任务大厅

| 类型 | 打卡限制 | 说明 |
|------|---------|------|
| 每日日常 | 每天限打卡1次 | 适合每天需要坚持的习惯 |
| 阶段里程碑 | 无次数限制 | 适合长期目标，可多次提交 |

**打卡流程**：点击「打卡」→ 等待管理员审批 → 通过后自动发放能量，可在「我的记录」查看进度。

### 星际心愿单

提交心愿后，管理员可批准或拒绝。批准后商品默认下架，需管理员在「商品管理」手动上架才能在商城兑换。

### 管理员功能

**发放星辰币**（管理中心 → 发放星辰币）

| 类型 | 能量变化 | 说明 |
|------|----------|------|
| 单星辰币 ⭐ | +1 | 普通表扬 |
| 双星辰币 🚀 | +5 | 优秀表现 |
| 陨石撞击 | −2 | 轻度惩罚 |
| 星暴气流 | −5 | 中度惩罚 |
| 黑洞吞噬 | −10 | 重度惩罚 |
| 自定义扣除 | 自定义 | 手动输入负整数，与预设互斥 |

发放后 **15 分钟内**可在记录列表中点击「后悔药」撤销，系统原子性回滚能量。

**商品管理**（仅舰长）：新建商品默认下架，需手动切换为上架后用户才可见。若商品存在兑换记录则无法删除，可将其下架代替删除。

**任务管理**：
- 「任务定义管理」：新增/编辑任务，设置名称、类型、奖励能量；舰长可指定专属审批人
- 「任务核验舱」：审批打卡，批准后自动发放能量，30% 概率触发碎片掉落，连续7天触发「星云爆发」
- 普通管理员只能看到自己创建的任务和自己负责审批的打卡记录

---

## 功能清单

### 已实现功能

**用户认证**
- [x] 用户登录（JWT Token，24 小时有效）
- [x] 用户注册（用户名唯一校验，密码 scrypt 加密存储）
- [x] 修改个人密码（需验证旧密码，修改后自动登出）
- [x] 管理员重置任意用户密码
- [x] 前端路由守卫 + 后端接口双重权限验证

**星辰币系统**
- [x] 发放单星辰币（+1）/ 双星辰币（+5）
- [x] 阶梯惩罚：陨石撞击（-2）/ 星暴气流（-5）/ 黑洞吞噬（-10）
- [x] 自定义大额扣分（手动输入负整数，与预设互斥）
- [x] 舰长寄语（选填，显示在孩子流水记录中）
- [x] 赋能官审计：每笔记录关联操作管理员（`admin_id`）
- [x] 扣分保护：可用能量最低归零，不产生负债
- [x] 后悔药：发放后 15 分钟内可撤销，原子性回滚

**飞船碎片 & 连击系统**
- [x] 打卡审批通过时 30% 概率掉落引擎🔧 / 雷达📡 / 船体🛡️ 碎片
- [x] 集齐三种碎片各1枚可升级飞船，等级驱动图标升阶
- [x] 连续完成任务7天触发「星云爆发」自动奖励 +10 能量
- [x] 连续3天无任务通过则每日自动扣除1点能量（衰减机制）

**任务大厅**
- [x] 任务类型：每日日常（限每天1次）/ 阶段里程碑（无限制）
- [x] 超级管理员可为任务指定专属审批人
- [x] 批准后自动发放能量并写入流水记录（含审计信息）
- [x] 普通管理员只能管理自己创建的任务、只能审批自己负责的打卡

**能量商城**
- [x] 商品 CRUD、图片上传、上下架、盲盒开关、排序权重
- [x] 盲盒兑换：随机抽取预设奖池中的奖品，结果写入兑换记录备注
- [x] 兑换前能量/库存双重校验，一次兑换多件
- [x] 取消兑换：退回能量 + 恢复库存

**其他**
- [x] 星际心愿单：提交/审批，批准后自动写入商品表
- [x] 6 款预设头像 + 本地图片上传
- [x] ECharts 能量累计趋势折线图
- [x] Docker Compose 一键部署
- [x] APScheduler 自动能量衰减（每日 00:05）+ 数据库备份（每日 03:00）
- [x] 星际广播台：WebSocket 局域网音箱接入，即时发分播报，APScheduler 驱动的早晚定时简报，播报目标可配置

### 技术指标

| 项目 | 数量 |
|------|------|
| 数据表 | 8 张 |
| 后端 API 接口 | 40 个 |
| 前端页面组件 | 19 个 |

### 后续扩展方向

| 优先级 | 功能 |
|--------|------|
| P1 | 积分排行榜 |
| P1 | 兑换记录 / 流水导出 Excel |
| P2 | 站内消息通知（发放星辰币时推送） |
| P2 | 商品分类管理 |
| P2 | 积分过期机制 |
| P3 | 移动端深度适配 |
| P3 | 多租户（多家庭独立数据隔离） |
| P3 | 微信 / 企业微信登录 |

---

## 测试清单

### 测试前准备

- [ ] Docker 服务全部运行（`docker-compose ps`）
- [ ] 前端访问 `http://localhost:28000` 正常
- [ ] 后端 API `http://localhost:28001/api` 可达

### 用户认证
- [ ] 注册：填写必填字段后注册成功；重复用户名提示错误
- [ ] 登录：`admin/admin123` 跳管理员仪表板；`zhangsan/user123` 跳用户仪表板；错误密码提示错误
- [ ] 修改密码：旧密码错误时提示错误；修改成功后自动登出，新密码可登录
- [ ] 未登录访问内页，自动跳转 `/login`

### 用户功能
- [ ] 仪表板：4个统计卡片正常；ECharts折线图正常渲染；飞船改造舱显示等级/碎片/连击
- [ ] 我的能量：负数能量行红色高亮；扣5分及以上显示 ☄️ + 深红加粗；有舰长寄语的显示蓝色提示条
- [ ] 能量商城：盲盒商品显示金色卡片；库存0时显示「已售罄」；兑换成功后能量减少、库存减少
- [ ] 任务大厅：打卡后状态变「审核中」；每日任务同天重复打卡被拦截；「我的记录」显示历史打卡
- [ ] 星际心愿单：提交状态为「待审核」；批准/拒绝状态正确更新

### 管理员功能
- [ ] 发放星辰币：单/双星辰币正确增加能量；三档惩罚与自定义输入互斥；扣到0不变负数；「赋能官 ✨」列显示操作管理员
- [ ] 后悔药：15分钟内出现撤销按钮；撤销后能量恢复；超过15分钟按钮消失
- [ ] 飞船碎片：审批通过后有概率显示碎片掉落提示；首页碎片数量更新；集齐后可升级飞船
- [ ] 连击：连续完成任务连击天数递增；累计7天出现「星云爆发」+10能量流水记录
- [ ] 用户管理（舰长）：新增/编辑/重置密码/设置头像均正常
- [ ] 商品管理（舰长）：上传图片超5MB被拒绝；有兑换记录的商品无法删除
- [ ] 兑换管理（舰长）：取消兑换后能量退回、库存恢复
- [ ] 心愿审核（舰长）：批准后商品管理中可见新商品（下架状态）
- [ ] 任务核验舱：批准打卡后用户能量增加，流水中出现对应记录；驳回带确认框

### 权限隔离
- [ ] 普通用户访问 `/admin/*` 路由，被重定向到首页
- [ ] 普通管理员访问 `/admin/users`，被重定向到首页
- [ ] 普通管理员调用 `POST /api/products` 返回 403
- [ ] 普通管理员只能看到自己创建的任务
- [ ] 普通用户只能查看自己的流水和兑换记录

---

## 浏览器控制台错误说明

### 可忽略的警告

| 错误 | 原因 | 处理 |
|------|------|------|
| `Unchecked runtime.lastError: The message port closed...` | 浏览器扩展程序引起（翻译扩展、广告拦截等） | 可忽略，不影响功能 |
| `Uncaught (in promise) cancel` | 路由导航被取消（快速切换页面导致） | 可忽略，正常行为 |

### 需要处理的错误

| 错误 | 原因 | 解决方法 |
|------|------|---------|
| `401 UNAUTHORIZED` | Token 过期 / 未登录 / 密码错误 | 清除浏览器 localStorage，重新登录 |
| `Failed to load resource: net::ERR_CONNECTION_REFUSED` | 后端服务未启动 / 端口被占用 | 检查 `docker-compose ps`，查看 `docker-compose logs backend` |
| `Cannot read properties of null` | 数据未加载完成 | 确保已登录后刷新页面 |

### 调试技巧

- **查看网络请求**：F12 → Network 标签，操作功能，查看请求和响应
- **清除缓存**：F12 → 右键刷新按钮 → 清空缓存并硬性重新加载
- **Token 失效**：F12 → Application → Local Storage → 清除，重新登录

---

## 常见问题

**Q：数据库连接失败**  
检查 `backend/.env` 中的 `MYSQL_PASSWORD` 是否与 MySQL 实际密码一致，Docker 环境中 `MYSQL_HOST` 必须填 `db`（服务名），不能填 `localhost`。

**Q：首次启动数据库初始化失败**  
MySQL 容器首次启动较慢，backend 可能提前尝试连接而失败。等待约 30 秒后重启 backend：`docker-compose restart backend`。

**Q：登录时提示用户名或密码错误**  
使用 `docker-compose exec backend python reset_admin.py` 重置管理员密码。

**Q：商品图片 / 头像图片不显示**  
确认后端服务正在运行，且 `backend/uploads/` 和 `backend/uploads/avatars/` 目录存在且有写权限（Docker 挂载卷自动创建）。

**Q：前端请求 API 报跨域错误**  
后端已全局启用 CORS。若部署在不同域名，在 `backend/app.py` 的 `CORS(app)` 处添加 `origins` 参数指定允许的来源。

**Q：Docker 部署后界面空白**  
`docker-compose logs frontend` 确认前端 Vite 构建成功，检查 `frontend/nginx.conf` 中 `proxy_pass` 指向的后端服务名是否为 `backend`。

**Q：Token 失效或登录跳转异常**  
清除浏览器 localStorage（F12 → Application → Local Storage → 清除），重新登录。

**Q：普通管理员登录后看不到任务**  
普通管理员只能看到自己创建的任务。需由超级管理员创建任务并将其指定为审批人，或普通管理员自行在任务定义管理中新建任务。

**Q：兑换按钮是灰色的，点不了？**  
可能是可用能量不足或商品库存为0。请先查看「我的能量」页面确认当前可用能量。

**Q：心愿已批准，但商城里找不到对应商品？**  
商品批准后默认下架，需要管理员前往「商品管理」手动上架，上架后即可在商城看到。

**Q：我的可用能量被扣到0了，还会继续扣吗？**  
不会。系统设有保护机制，可用能量最低为0，不会变为负数，但流水记录会保留实际扣除值。

**Q：商品为什么不能删除？**  
若该商品存在任何兑换历史记录，系统会拒绝删除以保护完整历史。可将其下架代替删除。

**Q：飞船碎片怎么获得？**  
每次管理员审批通过打卡时，系统有30%的概率随机掉落一枚引擎🔧、雷达📡或船体🛡️碎片。

**Q：「星云爆发」是什么？**  
连续完成任务累计满7天时，系统自动额外奖励+10能量，并在流水中显示「星云爆发！」记录。

**Q：能量为什么突然少了1点？**  
若连续3天没有任务被审批通过，系统每天凌晨自动扣除1点能量（衰减保护机制）。保持活跃完成任务即可避免。

**Q：发错了星辰币怎么办？**  
管理员在「发放星辰币」页面的记录列表中，可以对15分钟内的记录点击「后悔药」按钮撤销，系统会原子性地回滚能量。

**Q：数据库备份在哪里？**  
备份文件存放在 `backend/backups/` 目录（容器内 `/app/backups/`），格式为 `YYYY-MM-DD.sql`，自动保留最近 7 份。

**Q：时间显示与实际不符**  
`docker-compose.yml` 中所有服务已配置 `TZ: Asia/Shanghai`，MySQL 也已设置 `--default-time-zone='+08:00'`。如有问题请确认 Docker 宿主机时区设置。

---

## 更新日志

### v2.2.0 (2026-05-24)

#### 新增功能
- 星际广播台：通过 WebSocket 连接局域网音箱，即时发分语音播报（发放正能量 / 任务审批通过时触发）
- 定时星际简报：APScheduler 驱动的每日早晚简报，包含当前能量与心愿追踪，时间可动态配置无需重启
- 系统设置页面（`/admin/broadcast-settings`）：音箱 IP、端口（默认 18888）、心跳间隔、播报开关、播报目标配置，仅超级管理员可访问
- 一键测试广播：保存配置后可立即发送测试语音，最多等待 5 秒确认连接

#### 数据库变更
- 新增 `system_settings` 表（`speaker_ip`、`speaker_port`、`heartbeat_interval`、`enable_broadcast`、`enable_timed_broadcast`、`morning_broadcast_time`、`evening_broadcast_time`、`broadcast_targets`）

---

### v2.1.0 (2026-05-23)

#### 新增功能
- 飞船碎片系统：打卡审批通过时 30% 概率掉落三种碎片，集齐可升级飞船
- 连击系统：每日打卡累计7天触发「星云爆发」额外 +10 能量
- 能量衰减：连续3天无任务通过，每日凌晨自动扣除1点（APScheduler 定时任务）
- 后悔药：发放星辰币后15分钟内可一键撤销，原子性回滚
- 自动数据库备份：每日 03:00 自动 mysqldump 并保留最近7份
- 管理员仪表板（AdminDashboard）：待办雷达、舰队成员概览、全站动态时间轴

#### 数据库变更
- `users` 表新增 `fragments`（JSON）、`ship_level`、`streak_days`、`last_active_date`
- `thumbs_records` 表新增 `is_deleted`（软删除字段，用于后悔药功能）

---

### v2.0.0 (2026-05-20)

#### 新增功能
- 任务大厅：任务模板管理、每日日常 / 阶段里程碑类型、打卡审批流程
- 阶梯惩罚：三档预设 + 自定义大额扣分，大额惩罚视觉强化
- 多级管理员体系：`is_super_admin` 字段区分舰长与领航员，前后端双重权限隔离
- 赋能官审计：`thumbs_records.admin_id` 记录操作管理员
- 任务专属审批人：`tasks.reviewer_id`，普通管理员权限隔离
- 头像系统：6款预设 emoji + 本地图片上传

#### 数据库变更
- `users` 表新增 `avatar`、`is_super_admin`
- `thumbs_records` 表新增 `admin_id`、`given_by`、`parent_message`
- 新增 `tasks` 表（含 `reviewer_id`、`created_by`）
- 新增 `task_logs` 表

---

### v1.1.0 (2024-10-17)

- 新增用户注册功能
- 管理员重置用户密码
- 商品图片本地上传（UUID 命名防路径穿越）
- 双星辰币积分调整：2 → 5 能量
- 配置文件改用环境变量（.env）

---

### v1.0.0 (2024-10-17)

首次发布，包含基础用户系统、星辰币系统、能量商城、商品管理、兑换管理、星际心愿单、数据可视化、Docker Compose 一键部署。
