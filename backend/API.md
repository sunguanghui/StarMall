# API 接口文档

## 基础信息

- 基础URL: `http://localhost:28001/api`
- 所有需要认证的接口都需要在请求头中携带 Token: `Authorization: Bearer <token>`

## 响应格式

```json
{
  "code": 200,
  "message": "成功",
  "data": {}
}
```

---

## 1. 认证相关

### 1.1 用户登录

**接口**: `POST /auth/login`

**请求参数**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "username": "admin",
      "real_name": "系统管理员",
      "role": "admin",
      "is_super_admin": true
    }
  }
}
```

### 1.2 获取当前用户信息

**接口**: `GET /auth/info`

**需要认证**: 是

**响应字段**: `id`, `username`, `real_name`, `email`, `phone`, `role`, `is_super_admin`, `avatar`, `total_points`, `available_points`

### 1.3 修改密码

**接口**: `POST /auth/change-password`

**需要认证**: 是

**请求参数**:
```json
{
  "old_password": "当前密码",
  "new_password": "新密码（至少6位）"
}
```

### 1.4 更新头像

**接口**: `POST /auth/avatar`

**需要认证**: 是

**请求参数**:
```json
{
  "avatar": "preset_1"
}
```

`avatar` 可为预设标识（`preset_1`~`preset_6`）或 `/uploads/avatars/xxx.jpg` 路径。

---

## 2. 用户管理

### 2.1 获取用户列表

**接口**: `GET /users`

**需要认证**: 是（管理员）

**查询参数**:
- `page`: 页码 (默认: 1)
- `per_page`: 每页数量 (默认: 20)
- `keyword`: 搜索关键词

### 2.2 创建用户

**接口**: `POST /users`

**需要认证**: 是（管理员）

**请求参数**:
```json
{
  "username": "zhangsan",
  "password": "123456",
  "real_name": "张三",
  "email": "zhangsan@example.com",
  "phone": "13800138000",
  "role": "user",
  "is_super_admin": false,
  "avatar": "preset_1"
}
```

> `is_super_admin` 只有超级管理员才能设置为 `true`。

### 2.3 更新用户信息

**接口**: `PUT /users/{user_id}`

**需要认证**: 是

> 普通用户只能更新自身信息；`is_super_admin` 字段仅超级管理员可修改。

### 2.4 重置用户密码

**接口**: `POST /users/{user_id}/reset-password`

**需要认证**: 是（管理员）

**请求参数**:
```json
{
  "new_password": "新密码（至少6位）"
}
```

### 2.5 获取管理员列表

**接口**: `GET /admins`

**需要认证**: 是（管理员）

**说明**: 返回所有 `role='admin'` 的用户，用于任务审批人下拉框。

---

## 3. 文件上传

### 3.1 上传头像

**接口**: `POST /upload/avatar`

**需要认证**: 是

**请求**: `multipart/form-data`，字段名 `file`

**响应**:
```json
{ "url": "/uploads/avatars/abc123.jpg" }
```

### 3.2 访问头像

**接口**: `GET /uploads/avatars/{filename}`

**需要认证**: 否

### 3.3 上传商品图片

**接口**: `POST /upload`

**需要认证**: 是

**请求**: `multipart/form-data`，字段名 `file`

### 3.4 访问商品图片

**接口**: `GET /uploads/{filename}`

**需要认证**: 否

---

## 4. 星辰币管理

### 4.1 发放/扣除星辰币

**接口**: `POST /thumbs`

**需要认证**: 是（管理员）

**请求参数（发放）**:
```json
{
  "user_id": 2,
  "thumb_type": "single",
  "reason": "积极参与团队活动",
  "parent_message": "舰长寄语（选填）"
}
```

**请求参数（阶梯扣除）**:
```json
{
  "user_id": 2,
  "thumb_type": "deduction",
  "points": -5,
  "reason": "未完成任务"
}
```

| `thumb_type` 值 | 说明 | `points` |
|----------------|------|---------|
| `single` | 单星辰币 | +1（固定） |
| `double` | 双星辰币 | +5（固定） |
| `deduction` | 阶梯扣除 | 由 `points` 字段指定（负整数） |

> 扣除时 `points` 为负整数，可用能量最低扣至 0，不会产生负债。每笔记录自动写入 `admin_id`（当前操作管理员）用于审计。

### 4.2 获取星辰币记录

**接口**: `GET /thumbs`

**需要认证**: 是

**查询参数**:
- `page`: 页码
- `per_page`: 每页数量
- `user_id`: 用户ID（可选，管理员可指定）

**响应字段**: `thumb_type`, `points`, `reason`, `parent_message`, `given_by_name`, `admin_id`, `admin_name`, `created_at`

### 4.3 获取星辰币统计

**接口**: `GET /thumbs/stats`

**需要认证**: 是

**查询参数**:
- `user_id`: 用户ID（可选，默认当前用户）

**响应**:
```json
{
  "code": 200,
  "data": {
    "total_points": 100,
    "available_points": 80,
    "used_points": 20,
    "single_thumbs": 50,
    "double_thumbs": 25,
    "total_thumbs": 75
  }
}
```

---

## 5. 商品管理

### 5.1 获取商品列表

**接口**: `GET /products`

**需要认证**: 否

**查询参数**:
- `page`, `per_page`, `status`（`on_shelf`/`off_shelf`）, `keyword`

### 5.2 获取商品详情

**接口**: `GET /products/{product_id}`

**需要认证**: 否

### 5.3 创建商品

**接口**: `POST /products`

**需要认证**: 是（**超级管理员**）

**请求参数**:
```json
{
  "name": "小米充电宝",
  "description": "10000mAh 快充移动电源",
  "image_url": "/uploads/xxx.jpg",
  "points_required": 50,
  "stock": 10,
  "status": "on_shelf",
  "sort_order": 1,
  "is_blind_box": false
}
```

### 5.4 更新商品信息

**接口**: `PUT /products/{product_id}`

**需要认证**: 是（**超级管理员**）

### 5.5 切换商品上下架状态

**接口**: `POST /products/{product_id}/toggle-status`

**需要认证**: 是（**超级管理员**）

### 5.6 删除商品

**接口**: `DELETE /products/{product_id}`

**需要认证**: 是（**超级管理员**）

---

## 6. 兑换管理

### 6.1 创建兑换记录

**接口**: `POST /exchanges`

**需要认证**: 是

**请求参数**:
```json
{
  "product_id": 1,
  "quantity": 1
}
```

### 6.2 获取兑换记录

**接口**: `GET /exchanges`

**需要认证**: 是

**查询参数**: `page`, `per_page`, `user_id`（管理员可用）, `status`

### 6.3 取消兑换

**接口**: `POST /exchanges/{record_id}/cancel`

**需要认证**: 是

---

## 7. 星际心愿单

### 7.1 提交心愿

**接口**: `POST /wishlists`

**需要认证**: 是

**请求参数**:
```json
{
  "title": "乐高积木",
  "expected_points": 80
}
```

### 7.2 获取心愿列表

**接口**: `GET /wishlists`

**需要认证**: 是

> 普通用户只返回自己的心愿；管理员返回全部。

### 7.3 批准心愿

**接口**: `POST /wishlists/{id}/approve`

**需要认证**: 是（**超级管理员**）

> 自动在商品表创建一件下架商品。

### 7.4 拒绝心愿

**接口**: `POST /wishlists/{id}/reject`

**需要认证**: 是（**超级管理员**）

---

## 8. 任务大厅

### 8.1 获取任务列表

**接口**: `GET /tasks`

**需要认证**: 是

**查询参数**:
- `include_inactive`: `true` 时包含停用任务（管理员用）

**权限说明**: 普通管理员只返回自己创建的任务；超级管理员返回全部。

### 8.2 创建任务

**接口**: `POST /tasks`

**需要认证**: 是（管理员）

**请求参数**:
```json
{
  "title": "完成今日阅读打卡",
  "type": "daily",
  "energy_reward": 1,
  "is_active": true,
  "reviewer_id": null
}
```

| 字段 | 说明 |
|------|------|
| `type` | `daily`（每日日常）或 `milestone`（阶段里程碑） |
| `reviewer_id` | 专属审批人 ID，`null` 表示所有管理员均可审批。仅超级管理员可设置。 |

### 8.3 更新任务

**接口**: `PUT /tasks/{id}`

**需要认证**: 是（管理员，且必须是任务创建者）

### 8.4 删除任务

**接口**: `DELETE /tasks/{id}`

**需要认证**: 是（管理员，且必须是任务创建者）

---

## 9. 打卡记录

### 9.1 提交打卡

**接口**: `POST /task-logs`

**需要认证**: 是

**请求参数**:
```json
{
  "task_id": 1
}
```

> 每日日常任务同一用户当天只能打卡一次，重复提交返回 400。

### 9.2 获取打卡记录

**接口**: `GET /task-logs`

**需要认证**: 是

**查询参数**:
- `page`, `per_page`
- `status`: `pending` / `approved` / `rejected`

**权限说明**: 普通用户只返回自己的记录；普通管理员返回自己负责审批的记录；超级管理员返回全部。

### 9.3 批准打卡

**接口**: `POST /task-logs/{id}/approve`

**需要认证**: 是（管理员）

> 批准后自动发放任务能量并写入 `thumbs_records`。

### 9.4 驳回打卡

**接口**: `POST /task-logs/{id}/reject`

**需要认证**: 是（管理员）

---

## 10. 统计数据

### 10.1 获取仪表板统计

**接口**: `GET /stats/dashboard`

**需要认证**: 是

**响应 (管理员)**:
```json
{
  "code": 200,
  "data": {
    "total_users": 100,
    "total_thumbs": 500,
    "total_exchanges": 200,
    "total_products": 20
  }
}
```

**响应 (普通用户)**:
```json
{
  "code": 200,
  "data": {
    "total_points": 100,
    "available_points": 80,
    "used_points": 20,
    "total_thumbs": 50,
    "total_exchanges": 10
  }
}
```

---

## 权限速查表

| 角色 | 标识 |
|------|------|
| 普通用户 | `role=user` |
| 普通管理员（领航员） | `role=admin`, `is_super_admin=false` |
| 超级管理员（舰长） | `role=admin`, `is_super_admin=true` |

| 接口 | 普通用户 | 普通管理员 | 超级管理员 |
|------|---------|-----------|-----------|
| 发放星辰币 | ✗ | ✓ | ✓ |
| 用户管理 | ✗ | ✗ | ✓ |
| 商品管理（写） | ✗ | ✗ | ✓ |
| 兑换管理（取消） | ✗ | ✗ | ✓ |
| 心愿审核 | ✗ | ✗ | ✓ |
| 任务创建/编辑 | ✗ | ✓（仅自己） | ✓ |
| 打卡审批 | ✗ | ✓（仅负责的） | ✓ |
| 设置审批人 | ✗ | ✗ | ✓ |
