<template>
  <div class="dashboard">

    <!-- 星际导航面板 -->
    <div class="galaxy-section">
      <!-- 动态星空背景层 -->
      <div class="stars-layer stars-slow"></div>
      <div class="stars-layer stars-fast"></div>

      <!-- 中心驾驶舱 -->
      <div class="cockpit">
        <div class="cockpit-ring"></div>
        <div class="cockpit-inner">
          <div class="cockpit-emoji">🚀</div>
          <div class="cockpit-name">{{ userStore.userInfo?.real_name || '飞行员' }}</div>
          <div class="cockpit-label">驾驶舱</div>
          <button class="cockpit-btn" @click="$router.push('/mall')">去兑换 ✨</button>
        </div>
      </div>

      <!-- 四颗能量星球 -->
      <div
        class="planet planet-1"
        @click="$router.push('/my-points')"
        title="点击查看能量详情"
      >
        <div class="planet-emoji">🏆</div>
        <div class="planet-value">{{ stats.total_points || 0 }}</div>
        <div class="planet-label">总能量</div>
      </div>

      <div
        class="planet planet-2"
        @click="$router.push('/my-points')"
        title="点击查看能量详情"
      >
        <div class="planet-emoji">⚡</div>
        <div class="planet-value">{{ stats.available_points || 0 }}</div>
        <div class="planet-label">可用能量</div>
      </div>

      <div
        class="planet planet-3"
        @click="$router.push('/my-points')"
        title="点击查看星辰币"
      >
        <div class="planet-emoji">⭐</div>
        <div class="planet-value">{{ stats.total_thumbs || 0 }}</div>
        <div class="planet-label">获得星辰币</div>
      </div>

      <div
        class="planet planet-4"
        @click="$router.push('/my-exchanges')"
        title="点击查看兑换记录"
      >
        <div class="planet-emoji">🛒</div>
        <div class="planet-value">{{ stats.total_exchanges || 0 }}</div>
        <div class="planet-label">兑换次数</div>
      </div>
    </div>

    <!-- 下方内容区 -->
    <el-row :gutter="20" style="margin-top: 12px;">
      <el-col :xs="24" :sm="12">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>{{ isAdmin ? '最近发放的星辰币' : '最近获得的星辰币' }}</span>
              <el-button text @click="$router.push('/my-points')">查看更多</el-button>
            </div>
          </template>
          <div class="table-wrapper">
            <el-table :data="recentThumbs" style="width: 100%" v-loading="thumbsLoading">
              <!-- 管理员视角：显示被操作对象 -->
              <el-table-column v-if="isAdmin" prop="user_name" label="被操作人" width="75" show-overflow-tooltip />
              <el-table-column prop="thumb_type_name" label="类型" width="75" show-overflow-tooltip />
              <el-table-column label="能量" width="55">
                <template #default="{ row }">
                  <span :class="{ 'negative-points': row.points < 0 }">{{ row.points }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="reason" label="原因" show-overflow-tooltip />
              <!-- 普通用户视角：显示操作人 -->
              <el-table-column v-if="!isAdmin" prop="given_by_name" label="操作人" width="70" show-overflow-tooltip />
              <el-table-column prop="created_at" label="时间" width="105">
                <template #default="{ row }">{{ row.created_at?.slice(5, 16) }}</template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>{{ isAdmin ? '最近兑换记录（全部）' : '最近兑换记录' }}</span>
              <el-button text @click="$router.push('/my-exchanges')">查看更多</el-button>
            </div>
          </template>
          <div class="table-wrapper">
            <el-table :data="recentExchanges" style="width: 100%" v-loading="exchangesLoading">
              <!-- 管理员视角：显示兑换人 -->
              <el-table-column v-if="isAdmin" prop="user_name" label="兑换人" width="70" show-overflow-tooltip />
              <el-table-column prop="product_name" label="商品" min-width="80" show-overflow-tooltip />
              <el-table-column prop="points_spent" label="能量" width="55" />
              <el-table-column prop="status_name" label="状态" width="65">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)" size="small">
                    {{ row.status_name }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="时间" width="105">
                <template #default="{ row }">{{ row.created_at?.slice(5, 16) }}</template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 能量收集趋势图表 -->
    <el-card class="content-card">
      <template #header>
        <span class="chart-title">⚡ 能量收集趋势</span>
      </template>
      <div ref="chartRef" class="chart-container" />
    </el-card>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import api from '@/utils/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const isAdmin = computed(() => userStore.userInfo?.role === 'admin')
const stats = ref({})
const recentThumbs = ref([])
const recentExchanges = ref([])
const thumbsLoading = ref(false)
const exchangesLoading = ref(false)
const chartRef = ref(null)
let chartInstance = null

const getStatusType = (status) => {
  const types = { pending: 'warning', completed: 'success', cancelled: 'info' }
  return types[status] || ''
}

const loadStats = async () => {
  try {
    const res = await api.get('/stats/dashboard')
    stats.value = res.data
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadRecentThumbs = async () => {
  thumbsLoading.value = true
  try {
    const params = { per_page: 5 }
    // 管理员只看自己发放的记录
    if (isAdmin.value) {
      params.given_by = userStore.userInfo.id
    }
    const res = await api.get('/thumbs', { params })
    recentThumbs.value = res.data.list
  } catch (error) {
    console.error('加载星辰币记录失败:', error)
  } finally {
    thumbsLoading.value = false
  }
}

const loadRecentExchanges = async () => {
  exchangesLoading.value = true
  try {
    const res = await api.get('/exchanges', { params: { per_page: 5 } })
    recentExchanges.value = res.data.list
  } catch (error) {
    console.error('加载兑换记录失败:', error)
  } finally {
    exchangesLoading.value = false
  }
}

const initChart = async () => {
  try {
    const params = { per_page: 30 }
    // 管理员图表也只显示自己发放的趋势
    if (isAdmin.value) {
      params.given_by = userStore.userInfo.id
    }
    const res = await api.get('/thumbs', { params })
    const records = res.data.list.slice().reverse()

    const dateMap = {}
    let cumulative = 0
    for (const r of records) {
      const date = r.created_at.slice(0, 10)
      cumulative += r.points
      dateMap[date] = cumulative
    }

    const dates = Object.keys(dateMap)
    const values = Object.values(dateMap)

    await nextTick()
    if (!chartRef.value) return
    chartInstance = echarts.init(chartRef.value)
    chartInstance.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: dates, axisLabel: { rotate: 30 } },
      yAxis: { type: 'value', name: isAdmin.value ? '发放能量' : '累计能量' },
      series: [{
        name: isAdmin.value ? '发放能量' : '累计能量',
        type: 'line',
        data: values,
        smooth: true,
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(255, 107, 157, 0.4)' },
              { offset: 1, color: 'rgba(255, 107, 157, 0.02)' }
            ]
          }
        },
        lineStyle: { color: '#FF6B9D', width: 3 },
        itemStyle: { color: '#FF6B9D', borderWidth: 3, borderColor: 'white' }
      }],
      grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true }
    })
  } catch (error) {
    console.error('加载图表数据失败:', error)
  }
}

onMounted(() => {
  loadStats()
  loadRecentThumbs()
  loadRecentExchanges()
  initChart()
  window.addEventListener('resize', () => chartInstance?.resize())
})

onBeforeUnmount(() => {
  chartInstance?.dispose()
  window.removeEventListener('resize', () => chartInstance?.resize())
})
</script>

<style scoped>
/* ===== 整体容器 ===== */
.dashboard {
  max-width: 1400px;
}

/* ===== 星际导航面板区域 ===== */
.galaxy-section {
  position: relative;
  min-height: 220px;
  border-radius: 32px;
  overflow: hidden;
  background: linear-gradient(160deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  margin-bottom: 8px;
  box-shadow: 0 20px 60px rgba(15, 12, 41, 0.4);
}

/* ===== 动态星空层 ===== */
.stars-layer {
  position: absolute;
  inset: -100% 0 0 0;
  height: 200%;
  width: 100%;
  pointer-events: none;
}

.stars-slow {
  background-image:
    radial-gradient(1px 1px at 10% 15%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 25% 40%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 40% 8%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 55% 30%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 55%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 82% 12%, #ffc 0%, transparent 100%),
    radial-gradient(1px 1px at 92% 45%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 5% 65%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 18% 80%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 33% 70%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 48% 85%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 60% 75%, #ffd 0%, transparent 100%),
    radial-gradient(1px 1px at 75% 90%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 88% 68%, #fff 0%, transparent 100%),
    radial-gradient(2px 2px at 95% 82%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 14% 50%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 37% 22%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 63% 48%, #ffd 0%, transparent 100%),
    radial-gradient(1px 1px at 78% 35%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 50% 60%, #fff 0%, transparent 100%);
  background-size: 100% 50%;
  animation: starDrift 80s linear infinite;
  opacity: 0.8;
}

.stars-fast {
  background-image:
    radial-gradient(1px 1px at 7% 20%, #adf 0%, transparent 100%),
    radial-gradient(1px 1px at 22% 55%, #fff 0%, transparent 100%),
    radial-gradient(2px 2px at 38% 35%, #ffd 0%, transparent 100%),
    radial-gradient(1px 1px at 52% 72%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 67% 18%, #adf 0%, transparent 100%),
    radial-gradient(1px 1px at 80% 60%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 90% 30%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 12% 88%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 28% 92%, #ffc 0%, transparent 100%),
    radial-gradient(1px 1px at 45% 78%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 58% 95%, #adf 0%, transparent 100%),
    radial-gradient(2px 2px at 72% 82%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 76%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 3% 42%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 96% 58%, #ffd 0%, transparent 100%);
  background-size: 100% 50%;
  animation: starDrift 50s linear infinite;
  opacity: 0.5;
}

@keyframes starDrift {
  from { transform: translateY(0); }
  to   { transform: translateY(50%); }
}

/* ===== 中心驾驶舱 ===== */
.cockpit {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.cockpit-ring {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px dashed rgba(255, 255, 255, 0.2);
  animation: rotateSlow 20s linear infinite;
}

@keyframes rotateSlow {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

.cockpit-inner {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(255, 255, 255, 0.25);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  animation: pulse 3s ease-in-out infinite;
  box-shadow: 0 0 40px rgba(255, 107, 157, 0.3), inset 0 0 20px rgba(255,255,255,0.05);
}

@keyframes pulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(255, 107, 157, 0.3), inset 0 0 20px rgba(255,255,255,0.05); }
  50%       { transform: scale(1.05); box-shadow: 0 0 60px rgba(255, 107, 157, 0.5), inset 0 0 30px rgba(255,255,255,0.1); }
}

.cockpit-emoji {
  font-size: 20px;
  line-height: 1;
}

.cockpit-name {
  font-size: 12px;
  font-weight: 900;
  color: white;
  text-shadow: 0 0 10px rgba(255,255,255,0.8);
}

.cockpit-label {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.65);
}

.cockpit-btn {
  margin-top: 4px;
  padding: 2px 8px;
  border-radius: 20px;
  border: none;
  background: linear-gradient(135deg, #FF6B9D, #FF8E53);
  color: white;
  font-size: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 3px 10px rgba(255, 107, 157, 0.5);
}

.cockpit-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 5px 16px rgba(255, 107, 157, 0.7);
}

.cockpit-btn:active {
  transform: scale(0.94);
}

/* ===== 能量星球通用样式 ===== */
.planet {
  position: absolute;
  width: 95px;
  height: 95px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  z-index: 5;
  border: 3px solid rgba(255, 255, 255, 0.25);
}

.planet:hover {
  transform: scale(1.08) !important;
  animation-play-state: paused;
}

.planet:active {
  transform: scale(0.94) !important;
}

.planet-emoji {
  font-size: 18px;
  line-height: 1;
}

.planet-value {
  font-size: 20px;
  font-weight: 900;
  color: white;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
  line-height: 1;
}

.planet-label {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
}

/* ===== 四颗星球位置与颜色 ===== */
.planet-1 {
  top: 6%;
  left: 6%;
  background: radial-gradient(circle at 35% 35%, #FFD200, #F7971E);
  box-shadow: 0 0 40px rgba(247, 151, 30, 0.5), 0 12px 30px rgba(0,0,0,0.3);
  animation: float 4s ease-in-out infinite 0s;
}

.planet-2 {
  bottom: 6%;
  left: 6%;
  background: radial-gradient(circle at 35% 35%, #7FFFD4, #4ECDC4, #44A08D);
  box-shadow: 0 0 40px rgba(78, 205, 196, 0.5), 0 12px 30px rgba(0,0,0,0.3);
  animation: float 4s ease-in-out infinite 1.6s;
}

.planet-3 {
  top: 6%;
  right: 6%;
  background: radial-gradient(circle at 35% 35%, #FFB3C8, #FF6B9D, #FF8E53);
  box-shadow: 0 0 40px rgba(255, 107, 157, 0.5), 0 12px 30px rgba(0,0,0,0.3);
  animation: float 4s ease-in-out infinite 0.8s;
}

.planet-4 {
  bottom: 6%;
  right: 6%;
  background: radial-gradient(circle at 35% 35%, #a78bfa, #667eea, #764ba2);
  box-shadow: 0 0 40px rgba(102, 126, 234, 0.5), 0 12px 30px rgba(0,0,0,0.3);
  animation: float 4s ease-in-out infinite 2.4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-14px); }
}

/* ===== 下方内容卡片 ===== */
.content-card {
  margin-bottom: 12px;
}

.table-wrapper {
  overflow-x: auto;
  max-height: 220px;
  overflow-y: auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 700;
  color: #444;
}

.chart-title {
  font-size: 16px;
  font-weight: 700;
  color: #444;
}

.negative-points {
  color: #f56c6c;
  font-weight: bold;
}

.chart-container {
  height: 220px;
  width: 100%;
}

/* ===== 平板适配 ===== */
@media (max-width: 1200px) {
  .planet {
    width: 80px;
    height: 80px;
  }
  .planet-value { font-size: 18px; }
  .cockpit-inner { width: 78px; height: 78px; }
}

/* ===== 移动端适配（切换为网格布局）===== */
@media (max-width: 768px) {
  .galaxy-section {
    min-height: auto;
    padding: 20px 16px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .stars-layer {
    inset: -100% 0 0 0;
    height: 200%;
  }

  /* 隐藏绝对定位 cockpit，移动端显示行内驾驶舱 */
  .cockpit {
    position: relative;
    top: auto; left: auto;
    transform: none;
    order: -1;
  }

  /* 四颗星球改为相对定位 2×2 网格 */
  .planet {
    position: relative;
    top: auto !important;
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
    width: 100%;
    height: auto;
    border-radius: 20px;
    flex-direction: row;
    gap: 10px;
    padding: 14px 16px;
    animation: none;
  }

  .planet:hover { transform: scale(1.02) !important; }

  .planet-emoji { font-size: 24px; }
  .planet-value { font-size: 24px; }
  .planet-label { font-size: 13px; }

  /* 用 CSS grid 包裹所有星球 */
  .galaxy-section::after {
    content: none;
  }

  /* 用 JS-free 方式：让 .planet 自动流式排列 */
  .galaxy-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto;
    gap: 12px;
    padding: 16px;
  }

  .stars-layer {
    grid-column: 1 / -1;
    grid-row: 1 / -1;
    position: absolute;
    pointer-events: none;
    z-index: 0;
  }

  .cockpit {
    grid-column: 1 / -1;
    position: relative;
    z-index: 2;
  }

  .cockpit-inner {
    width: 100%;
    height: auto;
    border-radius: 20px;
    padding: 16px;
    flex-direction: row;
    gap: 12px;
  }

  .cockpit-ring { display: none; }

  .planet { z-index: 2; }
}
</style>
