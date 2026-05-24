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

      <div class="table-scroll-wrapper">
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

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="loadRecords"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'

const records = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterStatus = ref('pending')
const operating = ref(null)

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

onMounted(() => { loadRecords() })
</script>

<style scoped>
.exchange-delivery { max-width: 1200px; }
.page-header { margin-bottom: 20px; }
.page-title { font-size: 22px; font-weight: 900; color: #333; margin: 0 0 6px; }
.page-subtitle { color: #999; margin: 0; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
.text-muted { color: #ccc; font-size: 13px; }
.table-scroll-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }
</style>
