<template>
  <div class="help-page">
    <!-- 标题区 -->
    <div class="help-hero">
      <div class="hero-icon">🚀</div>
      <h1>星际航行指南</h1>
      <p>欢迎来到星途补给站，这里是你的飞行手册！</p>
    </div>

    <!-- 快速导航卡片 -->
    <el-row :gutter="16" class="nav-cards">
      <el-col :xs="12" :sm="8" :md="4" v-for="item in navItems" :key="item.id">
        <div class="nav-card" @click="scrollTo(item.id)">
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </div>
      </el-col>
    </el-row>

    <!-- 能量说明 -->
    <el-card class="section-card" id="section-energy">
      <template #header><div class="section-header">⚡ 能量说明</div></template>
      <el-table :data="energyData" border style="width:100%">
        <el-table-column prop="name" label="名称" width="120" />
        <el-table-column prop="desc" label="说明" />
      </el-table>
    </el-card>

    <!-- 账号管理 -->
    <el-card class="section-card" id="section-account">
      <template #header><div class="section-header">👨‍🚀 账号管理</div></template>
      <el-collapse accordion>
        <el-collapse-item title="🔑 登录" name="login">
          <p>访问系统首页，输入用户名和密码后点击「登录」。</p>
          <el-alert type="info" :closable="false" style="margin-top:10px">
            <template #title>
              <span>初始账号：超级管理员 <b>admin / admin123</b>，普通用户 <b>zhangsan / user123</b></span>
            </template>
          </el-alert>
        </el-collapse-item>
        <el-collapse-item title="✨ 注册" name="register">
          <el-table :data="registerData" border size="small">
            <el-table-column prop="field" label="字段" width="110" />
            <el-table-column prop="required" label="必填" width="70" />
            <el-table-column prop="rule" label="要求" />
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="🔒 修改密码" name="password">
          <p>点击右上角头像，选择「修改密码」，填写当前密码和新密码（至少6位）。修改成功后需重新登录。</p>
        </el-collapse-item>
        <el-collapse-item title="🖼️ 头像设置" name="avatar">
          <p>点击右上角头像 → 「个人中心」，可选择6款宇宙主题预设头像（🚀 👨‍🚀 🌟 🪐 🛸 ⭐），或上传本地图片（jpg/png/gif/webp，不超过5MB）。管理员也可在用户管理中为任意用户设置头像。</p>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 首页仪表盘 -->
    <el-card class="section-card" id="section-dashboard">
      <template #header><div class="section-header">🏠 首页仪表盘</div></template>
      <p class="desc-text">登录后默认进入首页，展示你的星际能量全景：</p>
      <el-row :gutter="12" class="stat-cards">
        <el-col :span="6" v-for="s in dashStats" :key="s.name">
          <div class="stat-mini" :style="{ background: s.color }">
            <div class="stat-icon">{{ s.icon }}</div>
            <div class="stat-name">{{ s.name }}</div>
          </div>
        </el-col>
      </el-row>
      <p class="desc-text" style="margin-top:14px">底部趋势图展示你近期累计能量的增长曲线 📈</p>
    </el-card>

    <!-- 能量商城 -->
    <el-card class="section-card" id="section-mall">
      <template #header><div class="section-header">🛒 能量商城</div></template>
      <el-collapse accordion>
        <el-collapse-item title="浏览商品" name="browse">
          <p>以网格形式展示所有上架商品，包括图片、名称、所需能量和库存。标有 <b>🎁 盲盒</b> 标签的是神秘盲盒哦！</p>
        </el-collapse-item>
        <el-collapse-item title="兑换商品" name="exchange">
          <ol class="step-list">
            <li>点击商品卡片下方「立即兑换」（盲盒显示「🎁 开盲盒」）</li>
            <li>弹窗确认可用能量、所需能量、库存和兑换数量</li>
            <li>点击「确定」完成兑换，可用能量立即扣减</li>
          </ol>
        </el-collapse-item>
        <el-collapse-item title="兑换限制" name="limit">
          <el-table :data="exchangeLimitData" border size="small">
            <el-table-column prop="cond" label="条件" width="160" />
            <el-table-column prop="result" label="结果" />
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 我的能量 -->
    <el-card class="section-card" id="section-points">
      <template #header><div class="section-header">⭐ 我的能量</div></template>
      <p class="desc-text">查看完整能量流水记录，顶部汇总统计：</p>
      <el-table :data="pointsStatsData" border size="small" style="margin-bottom:14px">
        <el-table-column prop="name" label="统计项" width="130" />
        <el-table-column prop="desc" label="说明" />
      </el-table>
      <p class="desc-text">流水记录列：<b>类型、能量、原因、舰长寄语、赋能官 ✨、时间</b></p>
      <el-alert type="warning" :closable="false" style="margin-top:8px">
        <template #title>扣除5点及以上的记录会显示 ☄️ 图标并以深红加粗样式标注，移动端卡片变为红色背景。</template>
      </el-alert>
    </el-card>

    <!-- 兑换记录 -->
    <el-card class="section-card" id="section-exchanges">
      <template #header><div class="section-header">📦 兑换记录</div></template>
      <el-table :data="exchangeStatusData" border size="small">
        <el-table-column prop="status" label="状态" width="90" />
        <el-table-column prop="meaning" label="含义" />
      </el-table>
    </el-card>

    <!-- 星际心愿单 -->
    <el-card class="section-card" id="section-wishlist">
      <template #header><div class="section-header">🌟 星际心愿单</div></template>
      <el-collapse accordion>
        <el-collapse-item title="提交心愿" name="submit">
          <p>点击「提交新心愿」，填写心愿名称（必填）和期望能量（至少1）。提交后状态为「待审核」。</p>
        </el-collapse-item>
        <el-collapse-item title="心愿状态说明" name="wstatus">
          <el-table :data="wishlistStatusData" border size="small">
            <el-table-column prop="status" label="状态" width="90" />
            <el-table-column prop="meaning" label="含义" />
          </el-table>
          <el-alert type="warning" :closable="false" style="margin-top:10px">
            <template #title>批准后商品默认下架，需管理员手动上架才能在商城看到并兑换。</template>
          </el-alert>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 任务大厅 -->
    <el-card class="section-card" id="section-tasks">
      <template #header><div class="section-header">🎯 任务大厅</div></template>
      <el-collapse accordion>
        <el-collapse-item title="任务类型" name="task-types">
          <el-table :data="taskTypeData" border size="small">
            <el-table-column prop="type" label="类型" width="110" />
            <el-table-column prop="limit" label="打卡限制" width="130" />
            <el-table-column prop="desc" label="说明" />
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="打卡流程" name="task-flow">
          <ol class="step-list">
            <li>在「任务大厅」切换到对应标签页（每日日常 / 阶段里程碑）</li>
            <li>点击任务卡片上的「打卡」按钮提交记录</li>
            <li>状态变为「审核中」，等待管理员审批</li>
            <li>批准后自动发放对应能量，流水记录同步更新</li>
          </ol>
        </el-collapse-item>
        <el-collapse-item title="打卡状态说明" name="task-status">
          <el-table :data="taskStatusData" border size="small">
            <el-table-column prop="status" label="状态" width="90" />
            <el-table-column prop="meaning" label="含义" />
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="我的记录" name="task-records">
          <p>切换到「我的记录」标签页可查看所有历史打卡记录及其审批状态。</p>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 管理员功能 -->
    <el-card class="section-card" id="section-admin">
      <template #header><div class="section-header">⚙️ 管理员功能</div></template>
      <el-alert type="info" :closable="false" style="margin-bottom:12px">
        <template #title>
          <span><b>👑 超级管理员（舰长）</b>拥有全部权限；<b>领航员（普通管理员）</b>只能发放星辰币、管理自己创建的任务和打卡审批。</span>
        </template>
      </el-alert>
      <el-collapse accordion>
        <el-collapse-item title="8.1 用户管理（仅舰长）" name="admin-users">
          <p>路径：管理中心 → 用户管理。可新增、编辑、重置密码，支持为任意用户设置头像。支持用户名/姓名关键词搜索。创建管理员账号时可勾选「超级管理员」开关（需舰长权限）。</p>
        </el-collapse-item>
        <el-collapse-item title="8.2 发放星辰币" name="admin-thumbs">
          <el-table :data="thumbTypeData" border size="small" style="margin-bottom:10px">
            <el-table-column prop="type" label="类型" width="130" />
            <el-table-column prop="points" label="能量变化" width="90" />
            <el-table-column prop="desc" label="说明" />
          </el-table>
          <ol class="step-list">
            <li>选择目标用户</li>
            <li>选择星辰币类型（发放正能量 / 选择扣除力度）</li>
            <li>扣除时可选预设档位，也可手动输入自定义分值</li>
            <li>填写原因（必填），可附加「舰长寄语」</li>
            <li>点击「发放」完成操作；每笔记录关联「赋能官 ✨」审计信息</li>
          </ol>
          <el-alert type="warning" :closable="false" style="margin-top:8px">
            <template #title>可用能量最低扣至0，不会产生负债。</template>
          </el-alert>
        </el-collapse-item>
        <el-collapse-item title="8.3 商品管理（仅舰长）" name="admin-products">
          <el-table :data="productFieldData" border size="small">
            <el-table-column prop="field" label="字段" width="110" />
            <el-table-column prop="required" label="必填" width="60" />
            <el-table-column prop="desc" label="说明" />
          </el-table>
          <el-alert type="info" :closable="false" style="margin-top:10px">
            <template #title>新建商品默认下架，需手动切换为上架后用户才可见。</template>
          </el-alert>
        </el-collapse-item>
        <el-collapse-item title="8.4 兑换管理（仅舰长）" name="admin-exchanges">
          <p>查看所有用户兑换记录。仅对「已完成」状态可执行取消操作，取消后能量全额退回、库存恢复。</p>
        </el-collapse-item>
        <el-collapse-item title="8.5 心愿审核（仅舰长）" name="admin-wishlists">
          <p><b>批准</b>：自动创建对应下架商品（名称=心愿名称，能量=期望能量，库存=1），需再去商品管理手动上架。</p>
          <p><b>拒绝</b>：状态变为「已拒绝」，不创建任何商品。</p>
        </el-collapse-item>
        <el-collapse-item title="8.6 任务管理" name="admin-tasks">
          <p><b>任务管理</b>：可新增、编辑任务，设置任务名称、类型（每日/里程碑）、奖励能量；舰长还可指定专属审批人，不指定则所有舰长均可审批。</p>
          <p><b>打卡审批</b>：在「待审核打卡」列表中批准或驳回飞行员的打卡申请。批准后自动发放能量。</p>
          <el-alert type="info" :closable="false" style="margin-top:8px">
            <template #title>领航员只能看到自己创建的任务和自己负责审批的打卡记录。</template>
          </el-alert>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 常见问题 -->
    <el-card class="section-card" id="section-faq">
      <template #header><div class="section-header">❓ 常见问题</div></template>
      <el-collapse accordion>
        <el-collapse-item v-for="faq in faqData" :key="faq.q" :title="'Q：' + faq.q" :name="faq.q">
          <p>{{ faq.a }}</p>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <div class="help-footer">🚀 本手册根据系统实际功能生成，如有更新以界面为准。</div>
  </div>
</template>

<script setup>
const navItems = [
  { id: 'section-energy',    icon: '⚡', label: '能量说明' },
  { id: 'section-account',   icon: '👨‍🚀', label: '账号管理' },
  { id: 'section-dashboard', icon: '🏠', label: '首页' },
  { id: 'section-mall',      icon: '🛒', label: '能量商城' },
  { id: 'section-points',    icon: '⭐', label: '我的能量' },
  { id: 'section-exchanges', icon: '📦', label: '兑换记录' },
  { id: 'section-wishlist',  icon: '🌟', label: '心愿单' },
  { id: 'section-tasks',     icon: '🎯', label: '任务大厅' },
  { id: 'section-admin',     icon: '⚙️', label: '管理员' },
  { id: 'section-faq',       icon: '❓', label: '常见问题' },
]

const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const energyData = [
  { name: '总能量',     desc: '历史累计获得的全部能量，只增不减' },
  { name: '可用能量',   desc: '当前可用于兑换商品的余额（总能量减去已消耗部分）' },
  { name: '已消耗能量', desc: '通过兑换商品花掉的能量' },
]

const registerData = [
  { field: '用户名',   required: '必填', rule: '3～20个字符，不可重复' },
  { field: '密码',     required: '必填', rule: '至少6位' },
  { field: '确认密码', required: '必填', rule: '需与密码完全一致' },
  { field: '真实姓名', required: '必填', rule: '用于显示和记录' },
  { field: '邮箱',     required: '选填', rule: '格式需正确' },
  { field: '手机号',   required: '选填', rule: '—' },
]

const dashStats = [
  { name: '总能量',   icon: '🏆', color: 'linear-gradient(135deg,#FFD200,#F7971E)' },
  { name: '可用能量', icon: '⚡', color: 'linear-gradient(135deg,#7FFFD4,#44A08D)' },
  { name: '星辰币',   icon: '⭐', color: 'linear-gradient(135deg,#FFB3C8,#FF6B9D)' },
  { name: '兑换次数', icon: '🛒', color: 'linear-gradient(135deg,#a78bfa,#667eea)' },
]

const exchangeLimitData = [
  { cond: '库存为 0',     result: '按钮显示「已售罄」，不可点击' },
  { cond: '可用能量不足', result: '按钮置灰，不可点击' },
  { cond: '部分可兑换',   result: '兑换数量上限自动调整为最大可兑换件数' },
]

const pointsStatsData = [
  { name: '总能量',       desc: '累计获得' },
  { name: '可用能量',     desc: '当前余额' },
  { name: '已消耗',       desc: '兑换消耗的能量' },
  { name: '单星辰币数量', desc: '获得的单星辰币（+1能量）总次数' },
  { name: '双星辰币数量', desc: '获得的双星辰币（+5能量）总次数' },
]

const exchangeStatusData = [
  { status: '待处理', meaning: '兑换申请已提交，等待处理' },
  { status: '已完成', meaning: '兑换成功' },
  { status: '已取消', meaning: '兑换已被取消，能量已退回' },
]

const wishlistStatusData = [
  { status: '待审核', meaning: '已提交，等待管理员处理' },
  { status: '已批准', meaning: '管理员同意，已创建对应下架商品' },
  { status: '已拒绝', meaning: '管理员未通过本次申请' },
]

const taskTypeData = [
  { type: '每日日常', limit: '每天限打卡1次', desc: '适合需要每天坚持的习惯，同一任务当天重复提交会被拦截' },
  { type: '阶段里程碑', limit: '无次数限制', desc: '适合长期目标，可多次提交打卡，每次都需要管理员审批' },
]

const taskStatusData = [
  { status: '审核中', meaning: '打卡已提交，等待管理员审批' },
  { status: '已完成', meaning: '审批通过，能量已发放到账' },
  { status: '已驳回', meaning: '管理员驳回了本次打卡申请' },
]

const thumbTypeData = [
  { type: '单星辰币', points: '+1', desc: '普通表扬鼓励' },
  { type: '双星辰币', points: '+5', desc: '优秀表现奖励' },
  { type: '陨石撞击', points: '−2', desc: '轻度惩罚' },
  { type: '星暴气流', points: '−5', desc: '中度惩罚，流水显示 ☄️ 警示' },
  { type: '黑洞吞噬', points: '−10', desc: '重度惩罚，流水显示 ☄️ 警示' },
  { type: '自定义扣除', points: '自定义', desc: '手动输入扣除分值，与预设档位互斥' },
]

const productFieldData = [
  { field: '商品名称', required: '✓', desc: '—' },
  { field: '商品描述', required: '—', desc: '显示在商品卡片上' },
  { field: '商品图片', required: '—', desc: '支持 jpg/png/gif/webp，不超过5MB' },
  { field: '所需能量', required: '✓', desc: '兑换所需能量数，最小值1' },
  { field: '库存数量', required: '✓', desc: '为0时商城显示「已售罄」' },
  { field: '是否盲盒', required: '—', desc: '开启后兑换时随机分配奖品' },
  { field: '排序',     required: '—', desc: '数值越小排列越靠前' },
  { field: '状态',     required: '✓', desc: '上架 / 下架' },
]

const faqData = [
  { q: '兑换按钮是灰色的，点不了？',
    a: '可能是可用能量不足或商品库存为0。请先查看「我的能量」页面确认当前可用能量。' },
  { q: '兑换了盲盒，怎么知道抽到了什么？',
    a: '前往「兑换记录」页面，找到对应记录，「备注」列会显示本次抽中的具体奖品名称。' },
  { q: '心愿已批准，但商城里找不到对应商品？',
    a: '商品批准后默认下架，需要管理员前往「商品管理」手动上架，上架后即可在商城看到。' },
  { q: '我的可用能量被扣到0了，还会继续扣吗？',
    a: '不会。系统设有保护机制，可用能量最低为0，不会变为负数，但流水记录会保留实际扣除值。' },
  { q: '已完成的兑换可以退吗？',
    a: '只有管理员可以在「兑换管理」页面取消已完成的兑换，取消后能量全额退回，库存也会恢复。' },
  { q: '修改密码后为什么被强制退出了？',
    a: '修改密码是安全操作，完成后系统会清除当前登录状态，需用新密码重新登录。' },
  { q: '商品为什么不能删除？',
    a: '若该商品存在任何兑换历史记录，系统会拒绝删除以保护完整历史。可将其下架代替删除。' },
  { q: '普通管理员（领航员）登录后看不到任务？',
    a: '领航员只能看到自己创建的任务。需由舰长创建任务并将其指定为审批人，或领航员自行在任务管理中新建任务。' },
  { q: '任务打卡后没有发放能量？',
    a: '打卡提交后处于「审核中」状态，需等待管理员审批通过才会发放能量。请在「我的记录」中查看审批进度。' },
  { q: '每日日常任务今天已经打过卡了，还能再打吗？',
    a: '不能。每日日常任务每人每天限打卡1次，系统会自动拦截重复提交。阶段里程碑任务无此限制。' },
]
</script>

<style scoped>
.help-page {
  max-width: 900px;
  padding-bottom: 40px;
}

/* 标题区 */
.help-hero {
  text-align: center;
  padding: 32px 20px 24px;
  background: linear-gradient(135deg, rgba(255,107,157,0.12) 0%, rgba(123,104,238,0.12) 100%);
  border-radius: 24px;
  margin-bottom: 20px;
  border: 1px solid rgba(255,107,157,0.2);
}
.hero-icon { font-size: 52px; margin-bottom: 8px; }
.help-hero h1 {
  font-size: 26px;
  font-weight: 900;
  color: #7B68EE;
  margin: 0 0 8px;
  letter-spacing: 2px;
}
.help-hero p { color: #999; font-size: 14px; margin: 0; }

/* 快速导航 */
.nav-cards { margin-bottom: 20px; }
.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 8px;
  background: white;
  border-radius: 16px;
  cursor: pointer;
  border: 1px solid #f0e8ff;
  transition: all 0.25s ease;
  margin-bottom: 12px;
  box-shadow: 0 2px 10px rgba(123,104,238,0.08);
}
.nav-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(255,107,157,0.25);
  border-color: #FF6B9D;
}
.nav-icon { font-size: 24px; }
.nav-label { font-size: 12px; color: #666; font-weight: 600; }

/* 内容卡片 */
.section-card {
  margin-bottom: 16px;
  border-radius: 20px !important;
  border: 1px solid #f0e8ff !important;
  box-shadow: 0 4px 20px rgba(123,104,238,0.08) !important;
}
.section-header {
  font-size: 16px;
  font-weight: 800;
  color: #7B68EE;
  letter-spacing: 1px;
}
.desc-text { color: #555; font-size: 14px; line-height: 1.8; margin: 0 0 8px; }

/* 统计迷你卡 */
.stat-cards { margin-top: 12px; }
.stat-mini {
  border-radius: 16px;
  padding: 14px 8px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}
.stat-icon { font-size: 24px; margin-bottom: 4px; }
.stat-name { font-size: 12px; font-weight: 700; }

/* 步骤列表 */
.step-list {
  margin: 8px 0 0 16px;
  padding: 0;
  color: #555;
  font-size: 14px;
  line-height: 2;
}

/* 底部 */
.help-footer {
  text-align: center;
  color: #bbb;
  font-size: 13px;
  padding: 20px 0 0;
}

/* Element Plus 覆盖 */
:deep(.el-card__header) {
  padding: 14px 20px;
  background: linear-gradient(135deg, rgba(123,104,238,0.06), rgba(255,107,157,0.06));
  border-radius: 20px 20px 0 0;
}
:deep(.el-collapse-item__header) {
  font-size: 14px;
  font-weight: 600;
  color: #555;
}
:deep(.el-collapse-item__content) {
  font-size: 14px;
  color: #666;
  line-height: 1.8;
}
</style>
