<template>
  <div class="help-page">
    <div class="help-hero">
      <div class="hero-icon">🚀</div>
      <h1>星际航行指南</h1>
      <p>欢迎来到星途补给站，这里是你的星际探索手册！</p>
    </div>

    <el-row :gutter="16" class="nav-cards">
      <el-col :xs="12" :sm="8" :md="4" v-for="item in navItems" :key="item.id">
        <div class="nav-card" @click="scrollTo(item.id)">
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </div>
      </el-col>
    </el-row>

    <el-card class="section-card" id="section-energy">
      <template #header><div class="section-header">⚡ 能量说明</div></template>
      <el-table :data="energyData" border style="width:100%">
        <el-table-column prop="name" label="名称" width="120" />
        <el-table-column prop="desc" label="说明" />
      </el-table>
    </el-card>

    <el-card class="section-card" id="section-account">
      <template #header><div class="section-header">👨‍🚀 账号管理</div></template>
      <el-collapse accordion>
        <el-collapse-item title="🔑 登录通道" name="login">
          <p>系统提供双层入口，满足不同角色的登舰需求：</p>
          <ul class="step-list">
            <li><b>正面登舰控制台：</b>标准账号密码登录，供舰长、领航员及普通探索者使用。</li>
            <li><b>背面小宇航员快捷舱：</b>点击右上角翻转卡片，使用专属 3D 图形密码盘免密极速登入（底层采用哈希加密，绝对保护隐私）。</li>
          </ul>
        </el-collapse-item>
        <el-collapse-item title="✨ 注册与审批" name="register">
          <p>为了保卫舰队安全，系统实行<b>「新兵入伍审批制」</b>。新人在登舰控制台注册后，状态将被锁定为「待审批」。</p>
          <el-alert type="warning" :closable="false" style="margin-top:8px; margin-bottom: 8px;">
            <template #title>注册成功后无法直接登录，必须呼叫 👑 舰长 在后台【批准登舰】后方可正式进入系统。</template>
          </el-alert>
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
          <p>点击右上角头像 → 「个人中心」，可选择宇宙主题预设头像，或上传本地图片。管理员也可在用户管理中为任意用户设置头像。</p>
        </el-collapse-item>
      </el-collapse>
    </el-card>

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
      <p class="desc-text" style="margin-top:14px">底部趋势图展示近期累计能量增长曲线 📈；下方「飞船改造舱」展示飞船等级、碎片收集进度和连击天数。</p>
    </el-card>

    <el-card class="section-card" id="section-ship">
      <template #header><div class="section-header">🛸 飞船碎片 & 连击系统</div></template>
      <el-collapse accordion>
        <el-collapse-item title="飞船碎片掉落" name="fragments">
          <p class="desc-text">每次管理员审批通过打卡时，系统有 <b>30% 的概率</b>随机掉落一枚飞船碎片：</p>
          <el-table :data="fragmentData" border size="small">
            <el-table-column prop="icon" label="图标" width="60" />
            <el-table-column prop="part" label="碎片类型" width="110" />
            <el-table-column prop="desc" label="说明" />
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="飞船升级" name="ship-upgrade">
          <ol class="step-list">
            <li>集齐引擎🔧、雷达📡、船体🛡️ 碎片各至少 1 枚</li>
            <li>在首页「飞船改造舱」点击「立即升级飞船」</li>
            <li>消耗各 1 枚碎片，飞船等级 +1，图标随等级升阶</li>
          </ol>
        </el-collapse-item>
        <el-collapse-item title="连击系统" name="streak">
          <el-table :data="streakData" border size="small" style="margin-bottom:10px">
            <el-table-column prop="cond" label="情况" width="200" />
            <el-table-column prop="result" label="效果" />
          </el-table>
          <el-alert type="success" :closable="false">
            <template #title>每连续完成 7 天任务触发「星云爆发」：自动额外奖励 +10 能量并写入流水记录。</template>
          </el-alert>
        </el-collapse-item>
        <el-collapse-item title="能量衰减" name="decay">
          <p class="desc-text">系统每日凌晨自动检查：普通用户连续 <b>3 天</b>未完成任务（无审批通过记录），自动扣除 1 点可用能量并写入流水记录。保持活跃即可避免衰减。</p>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <el-card class="section-card" id="section-mall">
      <template #header><div class="section-header">🛒 能量商城</div></template>
      <el-collapse accordion>
        <el-collapse-item title="浏览商品" name="browse">
          <p>以网格形式展示所有上架商品。标有 <b>🎁 盲盒</b> 标签的是神秘概率盲盒！</p>
        </el-collapse-item>
        <el-collapse-item title="兑换商品" name="exchange">
          <ol class="step-list">
            <li>点击商品卡片下方「立即兑换」（盲盒显示「🎁 开盲盒」）</li>
            <li>弹窗确认可用能量、库存和兑换数量</li>
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

    <el-card class="section-card" id="section-points">
      <template #header><div class="section-header">⭐ 我的能量</div></template>
      <p class="desc-text">查看完整、高精度的能量流水记录：</p>
      <el-table :data="pointsStatsData" border size="small" style="margin-bottom:14px">
        <el-table-column prop="name" label="统计项" width="130" />
        <el-table-column prop="desc" label="说明" />
      </el-table>
      <p class="desc-text">流水记录列包含：<b>类型、能量、原因、舰长寄语、赋能官 ✨，以及精确到秒的发生时间</b>。</p>
      <el-alert type="warning" :closable="false" style="margin-top:8px">
        <template #title>扣除5点及以上的记录会显示 ☄️ 图标并以深红加粗样式标注，移动端卡片变为红色背景。</template>
      </el-alert>
    </el-card>

    <el-card class="section-card" id="section-wishlist">
      <template #header><div class="section-header">🌟 星际心愿单</div></template>
      <el-collapse accordion>
        <el-collapse-item title="心愿状态说明" name="wstatus">
          <el-table :data="wishlistStatusData" border size="small">
            <el-table-column prop="status" label="状态" width="90" />
            <el-table-column prop="meaning" label="含义" />
          </el-table>
          <el-alert type="info" :closable="false" style="margin-top:10px">
            <template #title>心愿批准后自动转化为商城货架商品（默认下架），需管理员手动上架即可兑换。</template>
          </el-alert>
        </el-collapse-item>
      </el-collapse>
    </el-card>

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
        <el-collapse-item title="打卡状态说明" name="task-status">
          <el-table :data="taskStatusData" border size="small">
            <el-table-column prop="status" label="状态" width="90" />
            <el-table-column prop="meaning" label="含义" />
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <el-card class="section-card" id="section-broadcast">
      <template #header><div class="section-header">📡 星际广播台 (沉浸式语音)</div></template>
      <el-alert type="info" :closable="false" style="margin-bottom:12px">
        <template #title><span>广播台配置与全局调度仅限 <b>👑 舰长</b>，路径：左侧边栏 → 星际广播台。</span></template>
      </el-alert>
      <el-collapse accordion>
        <el-collapse-item title="全局播报策略" name="broadcast-global">
          <p class="desc-text">在此设定播报的总体方针。包含<b>目标宇航员</b>的指定（留空则为全舰队广播）以及<b>即时发分开关</b>。</p>
          <ul class="step-list">
            <li>开启后，管理员手动发放星辰币或审批任务时，音箱将瞬间响起。</li>
            <li>播报文案自带完整语境，例如：<i>“领航员爸爸，为小宇航员彤彤，发放了1枚星辰币！当前余额：100枚。”</i></li>
          </ul>
        </el-collapse-item>
        <el-collapse-item title="定时星际简报" name="broadcast-timed">
          <p class="desc-text">系统可根据设定的早/晚时间，自动进行高精度的全屋广播盘点：</p>
          <ul class="step-list">
            <li>播报内容包含当前最新总能量余额。</li>
            <li>若存在待实现的心愿，会自动计算并播报距离目标还差多少枚星辰币。</li>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <el-card class="section-card" id="section-admin">
      <template #header><div class="section-header">⚙️ 舰队管理枢纽</div></template>
      <el-alert type="success" :closable="false" style="margin-bottom:12px">
        <template #title>
          <span><b>👑 舰长 (超级管理员)</b>：掌握 100% 绝对控制权与人事调整权。<br><b>👨‍🚀 领航员 (管理员)</b>：拥有完整的日常业务运营权（发分、任务审批、发货）。</span>
        </template>
      </el-alert>
      <el-collapse accordion>
        <el-collapse-item title="8.1 兵力与人事调动（仅舰长）" name="admin-users">
          <p>路径：用户管理。舰长可在此处理外网注册人员的<b>[批准登舰]</b>请求。在编辑用户时，可通过解锁的神圣权限锁，将家人的角色从“普通用户”跨级提拔为“管理员”。</p>
        </el-collapse-item>
        <el-collapse-item title="8.2 发放星辰币 & 后悔药" name="admin-thumbs">
          <el-table :data="thumbTypeData" border size="small" style="margin-bottom:10px">
            <el-table-column prop="type" label="类型" width="130" />
            <el-table-column prop="points" label="能量变化" width="90" />
            <el-table-column prop="desc" label="说明" />
          </el-table>
          <el-alert type="warning" :closable="false" style="margin-top:8px">
            <template #title>发放后 <b>15 分钟内</b>可点击记录行的「后悔药」按钮撤销，能量自动回滚，杜绝手滑。</template>
          </el-alert>
        </el-collapse-item>
        <el-collapse-item title="8.3 任务核验舱" name="admin-tasks">
          <p>审批宇航员打卡申请。批准后自动发放能量，并在底层触发音箱播报。同时具备 30% 概率的碎片掉落检测与连击核算。领航员权限经过隔离，只能审批自己负责的任务。</p>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <el-card class="section-card" id="section-faq">
      <template #header><div class="section-header">❓ 常见问题答疑</div></template>
      <el-collapse accordion>
        <el-collapse-item v-for="faq in faqData" :key="faq.q" :title="'Q：' + faq.q" :name="faq.q">
          <p>{{ faq.a }}</p>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <div class="help-footer">🚀 星途补给站 - 为家庭探索之旅赋能</div>
  </div>
</template>

<script setup>
const navItems = [
  { id: 'section-account',   icon: '👨‍🚀', label: '登舰指南' },
  { id: 'section-ship',      icon: '🛸', label: '碎片与连击' },
  { id: 'section-mall',      icon: '🛒', label: '能量商城' },
  { id: 'section-points',    icon: '⭐', label: '航行日志' },
  { id: 'section-tasks',     icon: '🎯', label: '任务大厅' },
  { id: 'section-broadcast', icon: '📡', label: '星际广播' },
  { id: 'section-admin',     icon: '⚙️', label: '指挥枢纽' },
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
  { field: '用户名',   required: '必填', rule: '3～20个字符，系统通行凭证' },
  { field: '密码',     required: '必填', rule: '至少6位安全密钥' },
  { field: '真实姓名', required: '必填', rule: '用于系统展示与音箱沉浸式播报' },
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
  { cond: '部分可兑换',   result: '上限自动调整为最大可兑换件数' },
]

const pointsStatsData = [
  { name: '总能量',       desc: '累计获得' },
  { name: '可用能量',     desc: '当前余额' },
  { name: '已消耗',       desc: '兑换消耗的能量' },
  { name: '单星辰币数量', desc: '获得的单星辰币（+1能量）总次数' },
]

const wishlistStatusData = [
  { status: '待审核', meaning: '已提交，等待舰长审批' },
  { status: '已批准', meaning: '舰长同意，已落入商城后台库' },
  { status: '已拒绝', meaning: '申请被驳回' },
]

const taskTypeData = [
  { type: '每日日常', limit: '每天限打卡1次', desc: '适合需要每天坚持的习惯，重复提交会被拦截' },
  { type: '阶段里程碑', limit: '无次数限制', desc: '适合长期目标，可多次提交，需逐次审批' },
]

const taskStatusData = [
  { status: '审核中', meaning: '已提交，等待领航员或舰长核验' },
  { status: '已完成', meaning: '核验通过，奖励发放到账，触发音箱播报' },
  { status: '已驳回', meaning: '申请未通过，需重新努力' },
]

const fragmentData = [
  { icon: '🔧', part: '引擎碎片', desc: '随机掉落，集满可参与飞船升级' },
  { icon: '📡', part: '雷达碎片', desc: '随机掉落，集满可参与飞船升级' },
  { icon: '🛡️', part: '船体碎片', desc: '随机掉落，集满可参与飞船升级' },
]

const streakData = [
  { cond: '今日首次打卡被审批通过', result: '连击天数 +1，更新活跃状态' },
  { cond: '同一天多次打卡通过', result: '连击天数不重复累加' },
  { cond: '中断超过1天', result: '连击天数重置为1' },
  { cond: '累计满7天', result: '触发「星云爆发」额外奖励 +10 能量' },
]

const thumbTypeData = [
  { type: '单星辰币', points: '+1', desc: '普通表扬鼓励' },
  { type: '双星辰币', points: '+5', desc: '优秀表现奖励' },
  { type: '陨石撞击', points: '−2', desc: '轻度惩罚' },
  { type: '黑洞吞噬', points: '−10', desc: '重度惩罚，流水显示 ☄️ 警示' },
  { type: '自定义扣除', points: '自定义', desc: '手动输入负数，不可产生负债' },
]

const faqData = [
  { q: '刚注册完为什么登录不进去，提示要等舰长批准？',
    a: '为防止陌生人越权潜入，系统采取严格的防线隔离。新用户注册后处于「待审批」状态，必须由家里的舰长在后台“用户管理”中点击批准后，方可登舰。' },
  { q: '小宇航员不想记密码怎么办？',
    a: '在登录界面右上角点击“切换至小宇航员快捷舱”，卡片翻转后，选择自己的头像并划出家长预设的“星际图形密码”即可秒速登入。' },
  { q: '兑换按钮是灰色的，点不了？',
    a: '可能是可用能量不足或商品库存为0。请先查看「我的能量」确认余额。' },
  { q: '兑换了盲盒，怎么知道抽到了什么？',
    a: '前往「兑换记录」页面，找到对应记录，「备注」列会显示本次抽中的具体奖品。' },
  { q: '我的可用能量被扣到0了，还会继续扣成负数吗？',
    a: '不会。系统设有保护机制，可用能量最低为0，不会产生负债。' },
  { q: '领航员（普通管理员）登录后怎么找不到广播台菜单？',
    a: '音箱网络参数和系统全局调度属于底层核心权限，为避免误操作，仅超级管理员（舰长）拥有访问该菜单的权限。' },
  { q: '任务打卡后没有立刻加能量？',
    a: '打卡提交后处于「审核中」状态，需等待长辈在「任务核验舱」审批通过才会下发奖励并触发全屋播报。' },
  { q: '发错星辰币了，会把音箱播报撤回吗？',
    a: '一旦发放，音箱会瞬间播报，覆水难收！但在能量账本上，你可以在 15 分钟内点击「后悔药」将积分和流水安全撤销。' },
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