<template>
  <div class="admin-wishlists">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>星际心愿审核</span>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="状态">
          <el-select v-model="statusFilter" placeholder="全部" clearable @change="loadWishlists">
            <el-option label="待审核" value="pending" />
            <el-option label="已批准" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadWishlists">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="wishlists" style="width: 100%" v-loading="loading">
        <el-table-column prop="user_name" label="提交用户" width="120" />
        <el-table-column prop="title" label="心愿名称" show-overflow-tooltip />
        <el-table-column prop="expected_points" label="期望能量" width="110" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">{{ row.status_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="180" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <template v-if="row.status === 'pending'">
              <el-button link type="success" @click="handleApprove(row)">批准</el-button>
              <el-button link type="danger" @click="handleReject(row)">拒绝</el-button>
            </template>
            <span v-else style="color: #ccc; font-size: 12px;">已处理</span>
          </template>
        </el-table-column>
      </el-table>

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
const statusFilter = ref('pending')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const statusTagType = (status) => {
  return { pending: 'warning', approved: 'success', rejected: 'info' }[status] || ''
}

const loadWishlists = async () => {
  loading.value = true
  try {
    const res = await api.get('/wishlists', {
      params: { page: page.value, per_page: pageSize.value, status: statusFilter.value || undefined }
    })
    wishlists.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('加载心愿列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleApprove = (row) => {
  ElMessageBox.confirm(
    `批准「${row.title}」后将自动创建商品（下架状态），需前往商品管理手动上架。确认批准？`,
    '批准心愿',
    { confirmButtonText: '批准', cancelButtonText: '取消', type: 'success' }
  ).then(async () => {
    try {
      const res = await api.post(`/wishlists/${row.id}/approve`)
      ElMessage.success(res.data.message)
      await loadWishlists()
    } catch (error) {
      console.error('批准失败:', error)
    }
  })
}

const handleReject = (row) => {
  ElMessageBox.confirm(`确认拒绝「${row.title}」？`, '拒绝心愿', {
    confirmButtonText: '确认拒绝',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await api.post(`/wishlists/${row.id}/reject`)
      ElMessage.success('已拒绝该心愿')
      await loadWishlists()
    } catch (error) {
      console.error('拒绝失败:', error)
    }
  })
}

onMounted(() => {
  loadWishlists()
})
</script>

<style scoped>
.admin-wishlists {
  max-width: 1400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
