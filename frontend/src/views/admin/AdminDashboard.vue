<template>
  <div class="admin-dashboard">
    <div class="page-header">
      <h2 class="page-title">🛸 舰队指挥中心</h2>
      <p class="page-subtitle">欢迎回来，{{ userStore.isSuperAdmin() ? '舰长' : '领航员' }} {{ userStore.userInfo?.real_name }}！</p>
    </div>

    <!-- 待办审批雷达 -->
    <el-row :gutter="16" class="radar-row">
      <el-col :xs="24" :sm="8">
        <div class="radar-card radar-task" @click="$router.push('/admin/task-approval')">
          <div class="radar-icon">✅</div>
          <div class="radar-content">
            <div class="radar-count" :class="{ 'has-pending': pendingTasks > 0 }">{{ pendingTasks }}</div>
            <div class="radar-label">待核验任务</div>
          </div>
          <div v-if="pendingTasks > 0" class="radar-badge">{{ pendingTasks }}</div>
          <el-button size="small" round type="primary" class="radar-btn">前往处理 →</el-button>
        </div>
      </el-col>
      <el-col :xs="24" :sm="8">
        <div class="radar-card radar-exchange" @click="$router.push('/admin/exchange-delivery')">
          <div class="radar-icon">📦</div>
          <div class="radar-content">
            <div class="radar-count" :class="{ 'has-pending': pendingExchanges > 0 }">{{ pendingExchanges }}</div>
            <div class="radar-label">待交付补给</div>
          </div>
          <div v-if="pendingExchanges > 0" class="radar-badge">{{ pendingExchanges }}</div>
          <el-button size="small" round type="warning" class="radar-btn">前往处理 →</el-button>
        </div>
      </el-col>
      <el-col :xs="24" :sm="8">
        <div class="radar-card radar-wishlist" @click="$router.push('/admin/wishlist-approval')">
          <div class="radar-icon">💫</div>
          <div class="radar-content">
            <div class="radar-count" :class="{ 'has-pending': pendingWishlists > 0 }">{{ pendingWishlists }}</div>
            <div class="radar-label">待解析蓝图</div>
          </div>
          <div v-if="pendingWishlists > 0" class="radar-badge">{{ pendingWishlists }}</div>
          <el-button size="small" round type="success" class="radar-btn">前往处理 →</el-button>
        </div>
      </el-col>
    </el-row>

    <!-- 待办预览列表 -->
    <el-row :gutter="16" style="margin-bottom:16px;" v-if="pendingItems.length > 0">
      <el-col :span="24">
        <el-card class="content-card">
          <template #header>
            <span class="section-title">🔔 最新待办事项</span>
          </template>
          <div class="pending-list">
            <div v-for="item in pendingItems" :key="item.key" class="pending-item" @click="$router.push(item.route)">
              <el-tag :type="item.tagType" size="small" class="pending-tag">{{ item.tag }}</el-tag>
              <span class="pending-text">{{ item.text }}</span>
              <span class="pending-time">{{ item.time }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16">
      <!-- 舰队成员概览 -->
      <el-col :xs="24" :lg="14">
        <el-card id="onboard-admin-crew" class="content-card">
          <template #header>
            <div class="card-header">
              <span class="section-title">👥 舰队成员概览</span>
              <el-button text @click="$router.push('/admin/users')" v-if="userStore.isSuperAdmin()">乘员编制管理</el-button>
            </div>
          </template>
          <div v-loading="crewLoading">
            <div v-if="crewMembers.length === 0 && !crewLoading" class="empty-tip">暂无宇航员数据</div>
            <div class="crew-grid">
              <div v-for="member in crewMembers" :key="member.id" class="crew-card">
                <div class="crew-avatar">
                  <span v-if="!isUrl(member.avatar)" class="crew-emoji">{{ getEmoji(member.avatar) }}</span>
                  <el-avatar v-else :size="48" :src="member.avatar" />
                </div>
                <div class="crew-info">
                  <div class="crew-name">{{ member.real_name }}</div>
                  <div class="crew-stats">
                    <span class="crew-energy">⚡ {{ member.available_points }}</span>
                    <span class="crew-total">总 {{ member.total_points }}</span>
                  </div>
                </div>
                <el-button
                  size="small"
                  type="primary"
                  round
                  class="crew-boost-btn"
                  @click.stop="openQuickBoost(member)"
                >赋能</el-button>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 近期全站动态 -->
      <el-col :xs="24" :lg="10">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span class="section-title">🌐 近期全站动态</span>
              <el-button text @click="$router.push('/admin/thumbs')">查看更多</el-button>
            </div>
          </template>
          <div v-loading="activityLoading">
            <el-timeline v-if="activities.length > 0">
              <el-timeline-item
                v-for="(item, index) in activities"
                :key="index"
                :timestamp="item.created_at"
                placement="top"
                :type="item.points > 0 ? 'success' : 'danger'"
                size="normal"
              >
                <div class="activity-text">
                  <span class="activity-giver">「{{ item.given_by_name }}」</span>
                  为
                  <span class="activity-receiver">「{{ item.user_name }}」</span>
                  <span :class="item.points > 0 ? 'activity-positive' : 'activity-negative'">
                    {{ item.points > 0 ? '发放了' : '扣除了' }} {{ Math.abs(item.points) }} 点能量
                  </span>
                </div>
                <div class="activity-reason">{{ item.reason }}</div>
              </el-timeline-item>
            </el-timeline>
            <div v-else-if="!activityLoading" class="empty-tip">暂无动态</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快速赋能弹窗 -->
    <el-dialog v-model="boostVisible" :title="`⚡ 快速赋能 — ${boostTarget?.real_name}`" :width="dialogWidth">
      <el-form :model="boostForm" label-width="80px">
        <el-form-item label="奖励类型">
          <el-radio-group v-model="boostForm.thumb_type">
            <el-radio value="single">⭐ 单星辰币 (+1)</el-radio>
            <el-radio value="double">🚀 双星辰币 (+5)</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="原因">
          <el-input v-model="boostForm.reason" placeholder="请输入赋能原因" />
        </el-form-item>
        <el-form-item label="寄语">
          <el-input v-model="boostForm.parent_message" placeholder="给宇航员写一句鼓励的话（选填）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="boostVisible = false" round>取消</el-button>
        <el-button type="primary" @click="submitBoost" :loading="boosting" round>⚡ 立即赋能</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/utils/api'

const userStore = useUserStore()

const presetMap = {
  preset_1: '🚀', preset_2: '👨‍🚀', preset_3: '🌟',
  preset_4: '🪐', preset_5: '🛸', preset_6: '⭐'
}
const isUrl = (v) => v && (v.startsWith('/') || v.startsWith('http'))
const getEmoji = (v) => (!v || isUrl(v)) ? '🚀' : (presetMap[v] || '🚀')

// 待办雷达
const pendingTasks = ref(0)
const pendingExchanges = ref(0)
const pendingWishlists = ref(0)
const pendingItems = ref([])

// 舰队成员
const crewMembers = ref([])
const crewLoading = ref(false)

// 全站动态
const activities = ref([])
const activityLoading = ref(false)

// 快速赋能
const boostVisible = ref(false)
const isMobile = ref(window.innerWidth <= 768)
const handleResize = () => { isMobile.value = window.innerWidth <= 768 }
const dialogWidth = computed(() => isMobile.value ? '92%' : '420px')
const boostTarget = ref(null)
const boosting = ref(false)
const boostForm = reactive({ thumb_type: 'single', reason: '', parent_message: '' })

const loadRadar = async () => {
  try {
    const [taskRes, exchangeRes, wishlistRes] = await Promise.all([
      api.get('/task-logs', { params: { status: 'pending', per_page: 5 } }),
      api.get('/exchanges', { params: { status: 'pending', per_page: 5 } }),
      api.get('/wishlists', { params: { status: 'pending', per_page: 5 } })
    ])

    pendingTasks.value = taskRes.data?.total || 0
    pendingExchanges.value = exchangeRes.data?.total || 0
    pendingWishlists.value = wishlistRes.data?.total || 0

    const items = []
    for (const log of (taskRes.data?.list || [])) {
      items.push({ key: `task-${log.id}`, tag: '任务打卡', tagType: 'primary', text: `${log.user_name} 提交了「${log.task_title}」`, time: log.created_at, route: '/admin/task-approval' })
    }
    for (const ex of (exchangeRes.data?.list || [])) {
      items.push({ key: `ex-${ex.id}`, tag: '兑换申请', tagType: 'warning', text: `${ex.user_name} 申请兑换「${ex.product_name}」`, time: ex.created_at, route: '/admin/exchange-delivery' })
    }
    for (const wl of (wishlistRes.data?.list || [])) {
      items.push({ key: `wl-${wl.id}`, tag: '心愿蓝图', tagType: 'success', text: `${wl.user_name} 提交了心愿「${wl.title}」`, time: wl.created_at, route: '/admin/wishlist-approval' })
    }
    items.sort((a, b) => new Date(b.time) - new Date(a.time))
    pendingItems.value = items.slice(0, 8)
  } catch (err) {
    console.error('加载待办雷达失败:', err)
  }
}

const loadCrew = async () => {
  crewLoading.value = true
  try {
    const res = await api.get('/users', { params: { role: 'user', per_page: 50 } })
    crewMembers.value = res.data?.list || []
  } catch (err) {
    console.error('加载舰队成员失败:', err)
  } finally {
    crewLoading.value = false
  }
}

const loadActivities = async () => {
  activityLoading.value = true
  try {
    const res = await api.get('/thumbs', { params: { per_page: 15 } })
    activities.value = res.data?.list || []
  } catch (err) {
    console.error('加载全站动态失败:', err)
  } finally {
    activityLoading.value = false
  }
}

const openQuickBoost = (member) => {
  boostTarget.value = member
  boostForm.thumb_type = 'single'
  boostForm.reason = ''
  boostForm.parent_message = ''
  boostVisible.value = true
}

const submitBoost = async () => {
  if (!boostForm.reason) { ElMessage.error('请输入赋能原因'); return }
  boosting.value = true
  try {
    await api.post('/thumbs', {
      user_id: boostTarget.value.id,
      thumb_type: boostForm.thumb_type,
      reason: boostForm.reason,
      parent_message: boostForm.parent_message
    })
    ElMessage.success(`⚡ 已为 ${boostTarget.value.real_name} 赋能成功！`)
    boostVisible.value = false
    await Promise.all([loadCrew(), loadActivities()])
  } catch (err) {
    ElMessage.error(err.response?.data?.message || '赋能失败')
  } finally {
    boosting.value = false
  }
}

onMounted(() => {
  loadRadar()
  loadCrew()
  loadActivities()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.admin-dashboard { max-width: 1400px; }

.page-header { margin-bottom: 20px; }
.page-title { font-size: 24px; font-weight: 900; color: #333; margin: 0 0 6px; }
.page-subtitle { color: #999; margin: 0; font-size: 14px; }

/* 待办雷达卡片 */
.radar-row { margin-bottom: 16px; }

.radar-card {
  position: relative;
  background: white;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  overflow: hidden;
  margin-bottom: 16px;
}
.radar-card:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,0.12); }

.radar-task { border-left: 4px solid #7B68EE; }
.radar-exchange { border-left: 4px solid #F7971E; }
.radar-wishlist { border-left: 4px solid #4ECDC4; }

.radar-icon { font-size: 36px; flex-shrink: 0; }

.radar-content { flex: 1; }
.radar-count {
  font-size: 36px;
  font-weight: 900;
  color: #ccc;
  line-height: 1;
}
.radar-count.has-pending { color: #FF6B9D; }
.radar-label { font-size: 13px; color: #999; margin-top: 4px; }

.radar-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #f56c6c;
  color: white;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radar-btn { align-self: flex-end; }

/* 待办预览 */
.pending-list { display: flex; flex-direction: column; gap: 10px; }
.pending-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: #FFF8F0;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s;
}
.pending-item:hover { background: #fff0f5; }
.pending-tag { flex-shrink: 0; }
.pending-text { flex: 1; font-size: 14px; color: #444; }
.pending-time { font-size: 12px; color: #bbb; flex-shrink: 0; }

/* 舰队成员 */
.crew-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.crew-card {
  background: linear-gradient(135deg, #f5f0ff, #fff8f0);
  border-radius: 16px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.2s ease;
}
.crew-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(123,104,238,0.15); }

.crew-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B9D22, #7B68EE22);
  border: 2px solid #7B68EE33;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
  overflow: hidden;
}
.crew-emoji { line-height: 1; }

.crew-info { flex: 1; min-width: 0; }
.crew-name { font-size: 14px; font-weight: 700; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.crew-stats { display: flex; gap: 8px; margin-top: 4px; }
.crew-energy { font-size: 12px; font-weight: 700; color: #FF6B9D; }
.crew-total { font-size: 12px; color: #bbb; }
.crew-boost-btn { flex-shrink: 0; }

/* 全站动态 */
.activity-text { font-size: 13px; line-height: 1.6; }
.activity-giver { color: #7B68EE; font-weight: 700; }
.activity-receiver { color: #FF6B9D; font-weight: 700; }
.activity-positive { color: #67c23a; font-weight: 600; }
.activity-negative { color: #f56c6c; font-weight: 600; }
.activity-reason { font-size: 12px; color: #999; margin-top: 2px; }

.content-card { margin-bottom: 16px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.section-title { font-size: 16px; font-weight: 700; color: #444; }
.empty-tip { text-align: center; color: #ccc; padding: 30px 0; font-size: 14px; }
</style>