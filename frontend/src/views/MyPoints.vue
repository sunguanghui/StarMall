<template>
  <div class="my-points">
    <el-card class="stats-card">
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-label">总能量</div>
          <div class="stat-value">{{ stats.total_points || 0 }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">可用能量</div>
          <div class="stat-value" style="color: #4ECDC4;">{{ stats.available_points || 0 }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">已消耗</div>
          <div class="stat-value" style="color: #F7971E;">{{ stats.used_points || 0 }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">单星辰币 ⭐</div>
          <div class="stat-value">{{ stats.single_thumbs || 0 }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">双星辰币 🚀</div>
          <div class="stat-value">{{ stats.double_thumbs || 0 }}</div>
        </div>
      </div>
    </el-card>

    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>星辰币流水</span>
        </div>
      </template>

      <!-- 桌面表格 -->
      <div v-if="!isMobile" class="table-wrapper">
        <el-table :data="records" style="width: 100%" v-loading="loading">
          <el-table-column prop="thumb_type_name" label="类型" width="150" />
          <el-table-column label="能量" width="120">
            <template #default="{ row }">
              <span :class="pointsClass(row.points)">
                <span v-if="row.points <= -5" class="big-punish-icon">☄️</span>{{ row.points }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="获得/扣除原因" show-overflow-tooltip>
            <template #default="{ row }">
              <div>{{ row.reason }}</div>
              <el-alert
                v-if="row.parent_message"
                :title="`舰长寄语：${row.parent_message}`"
                type="info"
                :closable="false"
                show-icon
                class="parent-message-alert"
              />
            </template>
          </el-table-column>
          <el-table-column prop="given_by_name" label="赋能官 ✨" width="120" />
          <el-table-column prop="created_at" label="时间" width="180" />
        </el-table>
      </div>

      <!-- 移动端卡片列表 -->
      <div v-else class="mobile-records" v-loading="loading">
        <div v-for="(row, index) in records" :key="index" class="record-card" :class="{ 'record-card-punish': row.points <= -5 }">
          <div class="record-card-top">
            <span class="record-type">{{ row.thumb_type_name }}</span>
            <span :class="['record-points', pointsClass(row.points)]">
              <span v-if="row.points <= -5" class="big-punish-icon">☄️</span>{{ row.points > 0 ? '+' : '' }}{{ row.points }}
            </span>
          </div>
          <div class="record-reason">{{ row.reason }}</div>
          <el-alert
            v-if="row.parent_message"
            :title="`舰长寄语：${row.parent_message}`"
            type="info"
            :closable="false"
            show-icon
            class="parent-message-alert"
          />
          <div class="record-meta">
            <span>✨ {{ row.given_by_name }}</span>
            <span>{{ row.created_at }}</span>
          </div>
        </div>
        <el-empty v-if="!loading && records.length === 0" description="暂无记录" />
      </div>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :layout="isMobile ? 'prev, pager, next' : 'total, prev, pager, next, jumper'"
        @current-change="loadRecords"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '@/utils/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const stats = ref({})
const records = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const isMobile = ref(window.innerWidth <= 768)

const handleResize = () => { isMobile.value = window.innerWidth <= 768 }

const pointsClass = (points) => {
  if (points <= -5) return 'big-negative-points'
  if (points < 0) return 'negative-points'
  return ''
}

const loadStats = async () => {
  try {
    const res = await api.get('/thumbs/stats')
    stats.value = res.data
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadRecords = async () => {
  loading.value = true
  try {
    const res = await api.get('/thumbs', {
      params: {
        page: page.value,
        per_page: pageSize.value,
        user_id: userStore.userInfo.id
      }
    })
    records.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('加载记录失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStats()
  loadRecords()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.my-points {
  max-width: 1400px;
}

.stats-card {
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #FF6B9D;
}

.table-card {
  margin-bottom: 20px;
}

.table-wrapper {
  overflow-x: auto;
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

.big-negative-points {
  color: #c0392b;
  font-weight: 900;
  font-size: 1.1em;
}

.big-punish-icon {
  margin-right: 2px;
}

.parent-message-alert {
  margin-top: 6px;
  padding: 4px 8px;
  font-size: 12px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 移动端卡片样式 */
.mobile-records {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 80px;
}

.record-card {
  background: linear-gradient(135deg, #FFF0F8 0%, #FFF8F0 100%);
  border-radius: 16px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  box-shadow: 0 4px 12px rgba(255, 107, 157, 0.08);
}

.record-card-punish {
  background: linear-gradient(135deg, #FFF0F0 0%, #FFE8E8 100%);
  border: 1px solid #f56c6c44;
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.15);
}

.record-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.record-type {
  font-size: 15px;
  font-weight: 700;
  color: #555;
}

.record-points {
  font-size: 22px;
  font-weight: 900;
  color: #FF6B9D;
}

.record-reason {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.record-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #aaa;
  margin-top: 4px;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-label {
    font-size: 12px;
  }

  .pagination {
    justify-content: center;
  }
}
</style>
