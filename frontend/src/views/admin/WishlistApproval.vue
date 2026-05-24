<template>
  <div class="wishlist-approval">
    <div class="page-header">
      <h2 class="page-title">💫 蓝图解析室</h2>
      <p class="page-subtitle">审核宇航员提交的奖品心愿，批准后自动加入补给物资库房</p>
    </div>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>心愿蓝图队列</span>
          <el-select v-model="filterStatus" size="small" style="width:120px" @change="loadWishlists">
            <el-option label="待解析" value="pending" />
            <el-option label="已批准" value="approved" />
            <el-option label="已驳回" value="rejected" />
            <el-option label="全部" value="" />
          </el-select>
        </div>
      </template>

      <div class="table-scroll-wrapper">
        <el-table :data="wishlists" v-loading="loading" style="width:100%">
          <el-table-column prop="user_name" label="宇航员" width="100" />
          <el-table-column prop="title" label="心愿蓝图名称" min-width="160" show-overflow-tooltip />
          <el-table-column prop="expected_points" label="期望能量" width="110">
            <template #default="{ row }">{{ row.expected_points }} ⚡</template>
          </el-table-column>
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="statusTagType(row.status)" size="small">{{ row.status_name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="提交时间" width="160" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <template v-if="row.status === 'pending'">
                <el-button link type="success" @click="handleApprove(row)">🔬 批准研发</el-button>
                <el-button link type="danger" @click="handleReject(row)">❌ 驳回申请</el-button>
              </template>
              <span v-else class="text-muted">已处理</span>
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
        @current-change="loadWishlists"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'

const wishlists = ref([])
const loading = ref(false)
const filterStatus = ref('pending')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const statusTagType = (status) => {
  return { pending: 'warning', approved: 'success', rejected: 'info' }[status] || ''
}

const loadWishlists = async () => {
  loading.value = true
  try {
    const params = { page: page.value, per_page: pageSize.value }
    if (filterStatus.value) params.status = filterStatus.value
    const res = await api.get('/wishlists', { params })
    wishlists.value = res.data?.list || []
    total.value = res.data?.total || 0
  } catch { ElMessage.error('加载心愿列表失败') }
  finally { loading.value = false }
}

const handleApprove = (row) => {
  ElMessageBox.confirm(
    `批准「${row.title}」后将自动创建下架商品，需前往补给物资库房手动上架。确认批准研发？`,
    '🔬 批准研发',
    { confirmButtonText: '批准', cancelButtonText: '取消', type: 'success' }
  ).then(async () => {
    try {
      const res = await api.post(`/wishlists/${row.id}/approve`)
      ElMessage.success(res.data.message || '蓝图已批准，补给物资已录入库房')
      await loadWishlists()
    } catch (err) { ElMessage.error(err.response?.data?.message || '操作失败') }
  }).catch(() => {})
}

const handleReject = (row) => {
  ElMessageBox.confirm(`确认驳回「${row.title}」申请？`, '❌ 驳回申请', {
    confirmButtonText: '确认驳回',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await api.post(`/wishlists/${row.id}/reject`)
      ElMessage.success('申请已驳回')
      await loadWishlists()
    } catch (err) { ElMessage.error(err.response?.data?.message || '操作失败') }
  }).catch(() => {})
}

onMounted(() => { loadWishlists() })
</script>

<style scoped>
.wishlist-approval { max-width: 1200px; }
.page-header { margin-bottom: 20px; }
.page-title { font-size: 22px; font-weight: 900; color: #333; margin: 0 0 6px; }
.page-subtitle { color: #999; margin: 0; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
.text-muted { color: #ccc; font-size: 13px; }
.table-scroll-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }
</style>
