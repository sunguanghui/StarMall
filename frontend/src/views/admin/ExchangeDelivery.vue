<template>
  <div class="exchange-delivery">
    <div class="page-header">
      <h2 class="page-title">📦 补给调度室</h2>
      <p class="page-subtitle">处理宇航员的补给兑换申请，确认交付后自动完成发货</p>
    </div>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>兑换发货队列</span>
          <el-select v-model="filterStatus" size="small" style="width:120px" @change="loadRecords">
            <el-option label="待交付" value="pending" />
            <el-option label="已交付" value="completed" />
            <el-option label="已取消" value="cancelled" />
            <el-option label="全部" value="" />
          </el-select>
        </div>
      </template>

      <!-- ===== PC 端表格（> 768px） ===== -->
      <div class="table-scroll-wrapper pc-table-view">
        <el-table :data="records" v-loading="loading" style="width:100%">
          <el-table-column prop="user_name" label="宇航员" width="100" />
          <el-table-column prop="product_name" label="补给物资" min-width="150" show-overflow-tooltip />
          <el-table-column prop="quantity" label="数量" width="70" />
          <el-table-column prop="points_spent" label="消耗能量" width="100">
            <template #default="{ row }">{{ row.points_spent }} ⚡</template>
          </el-table-column>
          <el-table-column prop="status_name" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="statusTagType(row.status)" size="small">{{ row.status_name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" show-overflow-tooltip />
          <el-table-column prop="created_at" label="申请时间" width="160" />
          <el-table-column label="操作" width="160" fixed="right">
            <template #default="{ row }">
              <el-button
                v-if="row.status === 'pending'"
                link type="success"
                @click="handleDeliver(row)"
                :loading="operating === row.id"
              >🚀 确认交付</el-button>
              <el-button
                v-if="row.status === 'completed'"
                link type="danger"
                @click="handleCancel(row)"
                :loading="operating === row.id"
              >撤销交付</el-button>
              <span v-if="row.status === 'cancelled'" class="text-muted">已取消</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- ===== 移动端卡片列表（≤ 768px） ===== -->
      <div class="mobile-card-view mobile-card-list" v-loading="loading">
        <div
          v-for="row in records"
          :key="row.id"
          class="delivery-card"
          :class="{
            'delivery-card--pending':   row.status === 'pending',
            'delivery-card--completed': row.status === 'completed',
            'delivery-card--cancelled': row.status === 'cancelled'
          }"
        >
          <!-- 顶部：物资名 + 状态标签 -->
          <div class="delivery-card__top">
            <div class="delivery-card__product">
              <span class="delivery-card__icon">📦</span>
              <span class="delivery-card__name">{{ row.product_name }}</span>
            </div>
            <el-tag :type="statusTagType(row.status)" size="small" class="delivery-card__status">
              {{ row.status_name }}
            </el-tag>
          </div>

          <!-- 中部：宇航员、数量、消耗能量 -->
          <div class="delivery-card__meta">
            <div class="delivery-card__meta-item">
              <span class="meta-label">宇航员</span>
              <span class="meta-value">🧑‍🚀 {{ row.user_name }}</span>
            </div>
            <div class="delivery-card__meta-item">
              <span class="meta-label">数量</span>
              <span class="meta-value">× {{ row.quantity }}</span>
            </div>
            <div class="delivery-card__meta-item">
              <span class="meta-label">消耗能量</span>
              <span class="meta-value energy">{{ row.points_spent }} ⚡</span>
            </div>
          </div>

          <!-- 备注 -->
          <div v-if="row.remark" class="delivery-card__remark">
            💬 {{ row.remark }}
          </div>

          <!-- 申请时间 + 操作按钮 -->
          <div class="delivery-card__footer">
            <span class="delivery-card__time">🕐 {{ row.created_at }}</span>
            <div class="delivery-card__actions">
              <el-button
                v-if="row.status === 'pending'"
                type="success"
                size="small"
                :loading="operating === row.id"
                @click="handleDeliver(row)"
              >🚀 确认交付</el-button>
              <el-button
                v-if="row.status === 'completed'"
                type="danger"
                size="small"
                plain
                :loading="operating === row.id"
                @click="handleCancel(row)"
              >撤销交付</el-button>
              <span v-if="row.status === 'cancelled'" class="text-muted">已取消</span>
            </div>
          </div>
        </div>
        <el-empty v-if="!loading && records.length === 0" description="暂无发货记录" />
      </div>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :layout="isMobile ? 'prev, pager, next' : 'total, prev, pager, next'"
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
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterStatus = ref('pending')
const operating = ref(null)

const isMobile = ref(window.innerWidth <= 768)
const handleResize = () => { isMobile.value = window.innerWidth <= 768 }

const statusTagType = (status) => {
  return { pending: 'warning', completed: 'success', cancelled: 'info' }[status] || ''
}

const loadRecords = async () => {
  loading.value = true
  try {
    const params = { page: page.value, per_page: pageSize.value }
    if (filterStatus.value) params.status = filterStatus.value
    const res = await api.get('/exchanges', { params })
    records.value = res.data?.list || []
    total.value = res.data?.total || 0
  } catch { ElMessage.error('加载记录失败') }
  finally { loading.value = false }
}

const handleDeliver = async (row) => {
  operating.value = row.id
  try {
    await api.post(`/exchanges/${row.id}/complete`)
    ElMessage.success(`🚀 已确认交付「${row.product_name}」给 ${row.user_name}！`)
    await loadRecords()
  } catch (err) { ElMessage.error(err.response?.data?.message || '操作失败') }
  finally { operating.value = null }
}

const handleCancel = async (row) => {
  try {
    await ElMessageBox.confirm(
      `撤销交付「${row.product_name}」？能量将退回给 ${row.user_name}。`,
      '撤销确认',
      { type: 'warning' }
    )
    operating.value = row.id
    await api.post(`/exchanges/${row.id}/cancel`)
    ElMessage.success('已撤销交付，能量已退回')
    await loadRecords()
  } catch {}
  finally { operating.value = null }
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
.exchange-delivery { max-width: 1200px; }
.page-header { margin-bottom: 20px; }
.page-title { font-size: 22px; font-weight: 900; color: #333; margin: 0 0 6px; }
.page-subtitle { color: #999; margin: 0; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.text-muted { color: #ccc; font-size: 13px; }
.table-scroll-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }

/* ===== PC / 移动互斥 ===== */
.pc-only     { display: block; }
.mobile-only { display: none; }

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .pc-only     { display: none; }
  .mobile-only { display: block; }

  .pagination {
    justify-content: center;
    flex-wrap: wrap;
  }
}

/* --- 响应式双轨渲染强制隔离 --- */
/* 默认（PC端）：显示表格，隐藏卡片 */
.pc-table-view {
  display: block;
}
.mobile-card-view {
  display: none;
}

/* 移动端（屏幕宽度小于 768px）：隐藏表格，显示卡片 */
@media screen and (max-width: 767px) {
  .pc-table-view {
    display: none !important;
  }
  .mobile-card-view {
    display: block !important;
  }
}

/* ===== 移动端发货卡片 ===== */
.mobile-card-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 60px;
}

.delivery-card {
  border-radius: 16px;
  padding: 14px 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1.5px solid #e8e0f8;
  background: linear-gradient(135deg, #faf8ff 0%, #fff9f5 100%);
  box-shadow: 0 2px 10px rgba(123, 104, 238, 0.07);
}

.delivery-card--pending {
  border-color: #f0c060;
  background: linear-gradient(135deg, #fffdf0 0%, #fff8e0 100%);
}

.delivery-card--completed {
  border-color: #a0dba0;
  background: linear-gradient(135deg, #f0fff4 0%, #e8f8e8 100%);
}

.delivery-card--cancelled {
  border-color: #d0d0d0;
  background: linear-gradient(135deg, #f8f8f8 0%, #f0f0f0 100%);
  opacity: 0.75;
}

.delivery-card__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.delivery-card__product {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 0;
}

.delivery-card__icon {
  font-size: 20px;
  flex-shrink: 0;
}

.delivery-card__name {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delivery-card__status {
  flex-shrink: 0;
}

.delivery-card__meta {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.delivery-card__meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-label {
  font-size: 11px;
  color: #bbb;
}

.meta-value {
  font-size: 14px;
  font-weight: 600;
  color: #444;
}

.meta-value.energy {
  color: #FF6B9D;
  font-weight: 900;
}

.delivery-card__remark {
  font-size: 12px;
  color: #888;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 8px;
  padding: 6px 10px;
}

.delivery-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding-top: 8px;
}

.delivery-card__time {
  font-size: 12px;
  color: #bbb;
}

.delivery-card__actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
</style>
