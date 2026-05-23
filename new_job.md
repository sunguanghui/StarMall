# 角色与目标
你现在是 Claude Code。我们的「星途补给站」UI 已经改造得很漂亮了，现在需要增加一个核心的业务模块：**星际任务大厅 (Task/Quest System)**。
这个模块允许管理员发布习惯清单，普通用户（孩子）可以主动认领并提交完成申请，管理员审核后自动发放能量。

# 📋 任务大厅功能重构指南

## 1. 数据库设计 (Database Schema)
需要新建两张表：
- `tasks` (任务模板表)：字段包含 `id`, `title` (任务名称), `type` (枚举：'daily' 每日日常, 'milestone' 阶段里程碑), `energy_reward` (奖励能量值, 正整数), `is_active` (是否启用)。
- `task_logs` (任务执行记录表)：字段包含 `id`, `user_id`, `task_id`, `status` (枚举：'pending' 待审核, 'approved' 已批准, 'rejected' 已驳回), `created_at`, `updated_at`。

## 2. 后端逻辑 (Backend API)
- **任务管理 API**：管理员对 `tasks` 表的 CRUD 操作。
- **用户提交 API**：孩子端调用。**核心限制逻辑**：如果是 `daily` 类型的任务，后端必须校验该 `user_id` 在今天（当前日期 00:00:00 到 23:59:59）是否已经提交过该 `task_id`，若已提交则拦截。
- **审批 API**：管理员调用。将 `task_logs` 状态改为 `approved` 时，必须使用数据库事务，自动向 `thumbs_records` 表插入一条加分记录（原因自动关联任务名称），并给用户的可用能量加上对应的 `energy_reward`。

## 3. 前端视图 (Frontend Views)
- **孩子端 (`Tasks.vue` 建议命名为“任务大厅”)**：
  - 分区展示“日常巡航”和“主线探索”列表。
  - 每个任务卡片显示奖励的能量值（使用我们新设计的星球或能量图标）。
  - 点击“完成”后，按钮变成灰色“审核中”状态。
- **管理员端 (`AdminTasks.vue` 任务管理 & 审批)**：
  - 上半部分：管理任务库（发布新任务，设置每天还是阶段性）。
  - 下半部分：审批列表，展示孩子们提交的 pending 记录，提供“批准 (Approve)”和“驳回 (Reject)”按钮。

---

# 执行规则 (CRITICAL: TWO-STEP PROCESS)

**步骤 1：分析并提供方案 (Analyze & Propose)**
请思考如何将这个模块完美融入现有的路由体系中。输出一份《任务大厅架构实施方案》，明确列出：
1. 具体的 `CREATE TABLE` SQL 语句。
2. 打算新增或修改的后端 API 路由清单。
3. 打算新增的前端 Vue 文件名称和左侧菜单栏的菜单项名称。

**步骤 2：等待批准 (Wait for Approval)**
输出方案后立即停止。等待我回复 "Proceed" 后，再开始实际修改代码。