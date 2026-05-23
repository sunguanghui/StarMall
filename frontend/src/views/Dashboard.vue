<template>
  <div class="dashboard">
    <div class="stats-cards">
      <el-card class="stat-card stat-card-1" shadow="never">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon :size="32" color="white"><TrophyBase /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-title">总能量</p>
            <h2 class="stat-value">{{ stats.total_points || 0 }}</h2>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card stat-card-2" shadow="never">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon :size="32" color="white"><Wallet /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-title">可用能量</p>
            <h2 class="stat-value">{{ stats.available_points || 0 }}</h2>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card stat-card-3" shadow="never">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon :size="32" color="white"><Star /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-title">获得星辰币</p>
            <h2 class="stat-value">{{ stats.total_thumbs || 0 }}</h2>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card stat-card-4" shadow="never">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon :size="32" color="white"><ShoppingCart /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-title">兑换次数</p>
            <h2 class="stat-value">{{ stats.total_exchanges || 0 }}</h2>
          </div>
        </div>
      </el-card>
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>最近获得的星辰币</span>
              <el-button text @click="$router.push('/my-points')">查看更多</el-button>
            </div>
          </template>

          <el-table :data="recentThumbs" style="width: 100%" v-loading="thumbsLoading">
            <el-table-column prop="thumb_type_name" label="类型" width="130" />
            <el-table-column label="能量" width="80">
              <template #default="{ row }">
                <span :class="{ 'negative-points': row.points < 0 }">{{ row.points }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="reason" label="原因" show-overflow-tooltip />
            <el-table-column prop="created_at" label="时间" width="160" />
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>最近兑换记录</span>
              <el-button text @click="$router.push('/my-exchanges')">查看更多</el-button>
            </div>
          </template>

          <el-table :data="recentExchanges" style="width: 100%" v-loading="exchangesLoading">
            <el-table-column prop="product_name" label="商品" show-overflow-tooltip />
            <el-table-column prop="points_spent" label="能量" width="80" />
            <el-table-column prop="status_name" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ row.status_name }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="时间" width="160" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 能量收集趋势图表 -->
    <el-card class="content-card" style="margin-top: 0;">
      <template #header>
        <span>能量收集趋势</span>
      </template>
      <div ref="chartRef" class="chart-container" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { TrophyBase, Wallet, Star, ShoppingCart } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import api from '@/utils/api'

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
    const res = await api.get('/thumbs', { params: { per_page: 5 } })
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
    const res = await api.get('/thumbs', { params: { per_page: 30 } })
    const records = res.data.list.slice().reverse()

    // 按日期累计能量
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
      yAxis: { type: 'value', name: '累计能量' },
      series: [{
        name: '累计能量',
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
.dashboard {
  max-width: 1400px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  cursor: pointer;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  border-radius: 24px !important;
}

.stat-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.15) !important;
}

.stat-card-1 {
  background: linear-gradient(135deg, #FF6B9D 0%, #FF8E53 100%) !important;
}

.stat-card-2 {
  background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%) !important;
}

.stat-card-3 {
  background: linear-gradient(135deg, #F7971E 0%, #FFD200 100%) !important;
}

.stat-card-4 {
  background: linear-gradient(135deg, #A18CD1 0%, #FBC2EB 100%) !important;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 6px 0;
  font-weight: 500;
}

.stat-value {
  font-size: 36px;
  font-weight: 900;
  margin: 0;
  color: white;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.content-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 700;
  color: #444;
}

.negative-points {
  color: #f56c6c;
  font-weight: bold;
}

.chart-container {
  height: 280px;
  width: 100%;
}

@media (max-width: 1200px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
}
</style>
