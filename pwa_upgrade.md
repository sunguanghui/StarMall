# 角色与目标
你现在是 Claude Code。系统「星途补给站」的前端目前基于 Vue 3 + Vite 构建，且 UI 已经完成了童趣化改造。
现在的核心任务是：**将该前端项目升级为 PWA (渐进式 Web 应用)**，使其能够在手机和电脑端触发“添加到主屏幕/安装”的系统提示，拥有媲美原生 App 的独立运行窗口和体验。

# 🚀 PWA 改造实施指南 (必须在 frontend/ 目录下执行)

## 1. 安装核心依赖
- 请在 `frontend/` 目录中执行命令，安装 Vite 的 PWA 插件：`npm install vite-plugin-pwa -D`

## 2. 配置 Vite (vite.config.js)
- 引入 `VitePWA` 插件并将其添加到 `plugins` 数组中。
- **Manifest 配置要求**：
  - `name`: "星途补给站"
  - `short_name`: "星途补给"
  - `description`: "专属的家庭星际能量探索系统"
  - `theme_color`: "#ffffff" (或与当前童趣主题匹配的明快主色调)
  - `background_color`: "#ffffff"
  - `display`: "standalone" (必须，用于隐藏浏览器地址栏，实现 App 化)
  - `icons`: 配置基础的图标占位数组（如 192x192 和 512x512 的 PNG 引用），指向 `public/` 目录下的图标文件。
- **Service Worker 配置**：
  - `registerType`: 'autoUpdate' (确保每次代码更新后，用户的 App 能自动后台更新并接管)。

## 3. PWA 注册与注入 (main.js 或 index.html)
- 确保在前端入口文件（如 `frontend/src/main.js`）中引入 PWA 的虚拟模块自动注册逻辑。
- 添加代码：`import { registerSW } from 'virtual:pwa-register'`，并调用 `registerSW({ immediate: true })` 确保它在后台静默生效。

## 4. 图标占位符说明
- 由于你无法直接生成图片，请在 `frontend/public/` 目录下创建两个空的同名文本文件，分别重命名为 `pwa-192x192.png` 和 `pwa-512x512.png` 作为占位符。并输出一句提示，提醒我稍后用真实的图标文件替换它们。

---

# 执行规则 (CRITICAL: TWO-STEP PROCESS)

**步骤 1：分析并提供方案 (Analyze & Propose)**
请检查 `frontend/vite.config.js` 和 `frontend/src/main.js` 的当前结构。
输出一份简短的**《PWA 升级方案》**，说明你将如何修改这两个核心文件，以及你将配置的 Manifest 属性。

**步骤 2：等待批准 (Wait for Approval)**
输出方案后立即停止。等待我回复 "Proceed" 或 "批准" 后，再开始实际安装依赖和修改代码。确保所有代码修改都是完整的，不要有任何逻辑遗漏！