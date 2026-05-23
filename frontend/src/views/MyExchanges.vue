<template>
  <div class="my-exchanges">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的兑换记录</span>
        </div>
      </template>

      <!-- 桌面表格 -->
      <div v-if="!isMobile" class="table-wrapper">
        <el-table :data="records" style="width: 100%" v-loading="loading">
          <el-table-column prop="product_name" label="商品名称" show-overflow-tooltip />
          <el-table-column prop="quantity" label="数量" width="80" />
          <el-table-column prop="points_spent" label="消耗积分" width="100" />
          <el-table-column prop="status_name" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ row.status_name }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="兑换时间" width="180" />
          <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        </el-table>
      </div>

      <!-- 移动端卡片列表 -->
      <div v-else class="mobile-records" v-loading="loading">
        <div v-for="(row, index) in records" :key="index" class="record-card">
          <div class="record-card-top">
            <span class="record-product">{{ row.product_name }}</span>
            <el-tag :type="getStatusType(row.status)" size="small">{{ row.status_name }}</el-tag>
          </div>
          <div class="record-details">
            <span class="record-qty">× {{ row.quantity }} 件</span>
            <span class="record-points">⚡ {{ row.points_spent }}</span>
          </div>
          <div v-if="row.remark" class="record-remark">🎁 {{ row.remark }}</div>
          <div class="record-time">{{ row.created_at }}</div>
        </div>
        <el-empty v-if="!loading && records.length === 0" description="暂无兑换记录" />
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

const records = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const isMobile = ref(window.innerWidth <= 768)

const handleResize = () => { isMobile.value = window.innerWidth <= 768 }

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    completed: 'success',
    cancelled: 'info'
  }
  return types[status] || ''
}

const loadRecords = async () => {
  loading.value = true
  try {
    const res = await api.get('/exchanges', {
      params: {
        page: page.value,
        per_page: pageSize.value
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
  loadRecords()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.my-exchanges {
  max-width: 1400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 700;
  color: #444;
}

.table-wrapper {
  overflow-x: auto;
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
  background: linear-gradient(135deg, #FFF0F8 0%, #F0F8FF 100%);
  border-radius: 16px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(161, 140, 209, 0.1);
}

.record-card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.record-product {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  flex: 1;
  line-height: 1.4;
}

.record-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.record-qty {
  font-size: 14px;
  color: #888;
}

.record-points {
  font-size: 20px;
  font-weight: 900;
  color: #FF6B9D;
}

.record-remark {
  font-size: 13px;
  color: #888;
  background: rgba(255, 107, 157, 0.08);
  padding: 6px 10px;
  border-radius: 10px;
}

.record-time {
  font-size: 12px;
  color: #aaa;
}

@media (max-width: 768px) {
  .pagination {
    justify-content: center;
  }
}
</style>
