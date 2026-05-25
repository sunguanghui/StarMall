<template>
  <div class="admin-exchanges">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>兑换管理</span>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="状态">
          <el-select v-model="status" placeholder="全部" clearable @change="loadRecords">
            <el-option label="待处理" value="pending" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadRecords">查询</el-button>
        </el-form-item>
      </el-form>

      <!-- ===== PC 端表格（> 768px） ===== -->
      <div class="desktop-only-wrapper">
        <div class="table-scroll-wrapper">
          <el-table :data="records" style="width: 100%" v-loading="loading">
            <el-table-column prop="user_name" label="用户" width="120" />
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
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ row }">
                <el-button
                  link
                  type="danger"
                  @click="handleCancel(row)"
                  :disabled="row.status !== 'completed'"
                >取消兑换</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- ===== 移动端卡片列表（≤ 768px） ===== -->
      <div class="mobile-only-wrapper">
        <div class="mobile-card-list" v-loading="loading">
          <div
            v-for="row in records"
            :key="row.id"
            class="exchange-card"
            :class="{
              'exchange-card--pending':   row.status === 'pending',
              'exchange-card--completed': row.status === 'completed',
              'exchange-card--cancelled': row.status === 'cancelled'
            }"
          >
            <!-- 顶部：商品名 + 状态标签 -->
            <div class="exchange-card__top">
              <div class="exchange-card__product">
                <span class="exchange-card__icon">🛒</span>
                <span class="exchange-card__name">{{ row.product_name }}</span>
              </div>
              <el-tag :type="getStatusType(row.status)" size="small" class="exchange-card__status">
                {{ row.status_name }}
              </el-tag>
            </div>

            <!-- 中部：用户、数量、消耗积分 -->
            <div class="exchange-card__meta">
              <div class="exchange-card__meta-item">
                <span class="meta-label">用户</span>
                <span class="meta-value">🧑‍🚀 {{ row.user_name }}</span>
              </div>
              <div class="exchange-card__meta-item">
                <span class="meta-label">数量</span>
                <span class="meta-value">× {{ row.quantity }}</span>
              </div>
              <div class="exchange-card__meta-item">
                <span class="meta-label">消耗积分</span>
                <span class="meta-value meta-value--energy">{{ row.points_spent }} ⚡</span>
              </div>
            </div>

            <!-- 备注 -->
            <div v-if="row.remark" class="exchange-card__remark">
              💬 {{ row.remark }}
            </div>

            <!-- 底部：时间 + 操作 -->
            <div class="exchange-card__footer">
              <span class="exchange-card__time">🕐 {{ row.created_at }}</span>
              <el-button
                v-if="row.status === 'completed'"
                size="small"
                type="danger"
                plain
                @click="handleCancel(row)"
              >取消兑换</el-button>
              <span v-else class="text-muted">—</span>
            </div>
          </div>
          <el-empty v-if="!loading && records.length === 0" description="暂无兑换记录" />
        </div>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'

const records = ref([])
const loading = ref(false)
const status = ref('')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const isMobile = ref(window.innerWidth <= 768)
const handleResize = () => { isMobile.value = window.innerWidth <= 768 }

const getStatusType = (status) => {
  const types = { pending: 'warning', completed: 'success', cancelled: 'info' }
  return types[status] || ''
}

const loadRecords = async () => {
  loading.value = true
  try {
    const res = await api.get('/exchanges', {
      params: { page: page.value, per_page: pageSize.value, status: status.value }
    })
    records.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('加载记录失败:', error)
  } finally {
    loading.value = false
  }
}

const handleCancel = (row) => {
  ElMessageBox.confirm(
    `确定要取消 "${row.user_name}" 兑换的 "${row.product_name}" 吗？积分将退回给用户。`,
    '取消兑换',
    { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
  ).then(async () => {
    try {
      await api.post(`/exchanges/${row.id}/cancel`)
      ElMessage.success('兑换已取消，积分已退回')
      await loadRecords()
    } catch (error) {
      console.error('取消失败:', error)
    }
  })
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
.admin-exchanges { max-width: 1400px; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form { margin-bottom: 20px; }

.text-muted { color: #ccc; font-size: 13px; }

.table-scroll-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .search-form { margin-bottom: 12px; }

  .pagination {
    justify-content: center;
    flex-wrap: wrap;
  }
}

/* ===== 移动端兑换卡片 ===== */
.mobile-card-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 60px;
}

.exchange-card {
  border-radius: 16px;
  padding: 14px 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1.5px solid #e8e0f8;
  background: linear-gradient(135deg, #faf8ff 0%, #fff9f5 100%);
  box-shadow: 0 2px 10px rgba(123, 104, 238, 0.07);
}

.exchange-card--pending {
  border-color: #f0c060;
  background: linear-gradient(135deg, #fffdf0 0%, #fff8e0 100%);
}

.exchange-card--completed {
  border-color: #a0dba0;
  background: linear-gradient(135deg, #f0fff4 0%, #e8f8e8 100%);
}

.exchange-card--cancelled {
  border-color: #d0d0d0;
  background: linear-gradient(135deg, #f8f8f8 0%, #f2f2f2 100%);
  opacity: 0.7;
}

.exchange-card__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.exchange-card__product {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 0;
}

.exchange-card__icon { font-size: 18px; flex-shrink: 0; }

.exchange-card__name {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.exchange-card__status { flex-shrink: 0; }

.exchange-card__meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.exchange-card__meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-label { font-size: 11px; color: #bbb; }

.meta-value {
  font-size: 14px;
  font-weight: 600;
  color: #444;
}

.meta-value--energy {
  font-size: 16px;
  font-weight: 900;
  color: #FF6B9D;
}

.exchange-card__remark {
  font-size: 12px;
  color: #888;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 8px;
  padding: 6px 10px;
}

.exchange-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding-top: 8px;
  gap: 8px;
}

.exchange-card__time { font-size: 12px; color: #bbb; }

/* --- 响应式双轨渲染物理隔离 (终极版) --- */
.mobile-only-wrapper {
  display: none !important;
}

@media screen and (max-width: 768px) {
  .desktop-only-wrapper {
    display: none !important;
  }
  .mobile-only-wrapper {
    display: block !important;
  }
}
</style>
