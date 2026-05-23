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
          <div class="stat-value" style="color: #52c41a;">{{ stats.available_points || 0 }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">已消耗</div>
          <div class="stat-value" style="color: #faad14;">{{ stats.used_points || 0 }}</div>
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

      <el-table :data="records" style="width: 100%" v-loading="loading">
        <el-table-column prop="thumb_type_name" label="类型" width="150" />
        <el-table-column label="能量" width="100">
          <template #default="{ row }">
            <span :class="{ 'negative-points': row.points < 0 }">{{ row.points }}</span>
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
        <el-table-column prop="given_by_name" label="发放人" width="120" />
        <el-table-column prop="created_at" label="时间" width="180" />
      </el-table>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        @current-change="loadRecords"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const stats = ref({})
const records = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

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
  color: #1890ff;
}

.table-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.negative-points {
  color: #f56c6c;
  font-weight: bold;
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

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
