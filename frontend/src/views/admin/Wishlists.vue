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

      <!-- ===== PC 端表格（> 768px） ===== -->
      <div class="table-scroll-wrapper pc-table-view">
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
      </div>

      <!-- ===== 移动端卡片列表（≤ 768px） ===== -->
      <div class="mobile-card-list mobile-card-view" v-loading="loading">
        <div
          v-for="row in wishlists"
          :key="row.id"
          class="wish-card"
          :class="{
            'wish-card--pending':  row.status === 'pending',
            'wish-card--approved': row.status === 'approved',
            'wish-card--rejected': row.status === 'rejected'
          }"
        >
          <!-- 顶部：心愿名 + 状态标签 -->
          <div class="wish-card__top">
            <div class="wish-card__title-wrap">
              <span class="wish-card__icon">💫</span>
              <span class="wish-card__title">{{ row.title }}</span>
            </div>
            <el-tag :type="statusTagType(row.status)" size="small" class="wish-card__status">
              {{ row.status_name }}
            </el-tag>
          </div>

          <!-- 中部：提交用户 + 期望能量 -->
          <div class="wish-card__meta">
            <div class="wish-card__meta-item">
              <span class="meta-label">提交用户</span>
              <span class="meta-value">🧑‍🚀 {{ row.user_name }}</span>
            </div>
            <div class="wish-card__meta-item">
              <span class="meta-label">期望能量</span>
              <span class="meta-value meta-value--energy">{{ row.expected_points }} ⚡</span>
            </div>
          </div>

          <!-- 底部：时间 + 操作按钮 -->
          <div class="wish-card__footer">
            <span class="wish-card__time">🕐 {{ row.created_at }}</span>
            <div class="wish-card__actions">
              <template v-if="row.status === 'pending'">
                <el-button size="small" type="success" @click="handleApprove(row)">批准</el-button>
                <el-button size="small" type="danger" plain @click="handleReject(row)">拒绝</el-button>
              </template>
              <span v-else class="text-muted">已处理</span>
            </div>
          </div>
        </div>
        <el-empty v-if="!loading && wishlists.length === 0" description="暂无心愿记录" />
      </div>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :layout="isMobile ? 'prev, pager, next' : 'total, prev, pager, next'"
        @current-change="loadWishlists"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'

const wishlists = ref([])
const loading = ref(false)
const statusFilter = ref('pending')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const isMobile = ref(window.innerWidth <= 768)
const handleResize = () => { isMobile.value = window.innerWidth <= 768 }

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
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.admin-wishlists { max-width: 1400px; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form { margin-bottom: 20px; }

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

  .search-form { margin-bottom: 12px; }

  .pagination {
    justify-content: center;
    flex-wrap: wrap;
  }
}

/* --- 响应式双轨渲染强制隔离 --- */
.pc-table-view  { display: block; }
.mobile-card-view { display: none; }

@media screen and (max-width: 767px) {
  .pc-table-view  { display: none !important; }
  .mobile-card-view { display: block !important; }
}

/* ===== 移动端心愿卡片 ===== */
.mobile-card-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 60px;
}

.wish-card {
  border-radius: 16px;
  padding: 14px 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1.5px solid #e8d8f8;
  background: linear-gradient(135deg, #fdf8ff 0%, #fff5fd 100%);
  box-shadow: 0 2px 10px rgba(180, 100, 220, 0.07);
}

.wish-card--pending {
  border-color: #f0c060;
  background: linear-gradient(135deg, #fffdf0 0%, #fff8e0 100%);
}

.wish-card--approved {
  border-color: #a0dba0;
  background: linear-gradient(135deg, #f0fff4 0%, #e8f8e8 100%);
}

.wish-card--rejected {
  border-color: #d0d0d0;
  background: linear-gradient(135deg, #f8f8f8 0%, #f2f2f2 100%);
  opacity: 0.72;
}

.wish-card__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.wish-card__title-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 0;
}

.wish-card__icon { font-size: 18px; flex-shrink: 0; }

.wish-card__title {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.wish-card__status { flex-shrink: 0; }

.wish-card__meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.wish-card__meta-item {
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
  font-size: 18px;
  font-weight: 900;
  color: #c850c0;
}

.wish-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding-top: 8px;
}

.wish-card__time { font-size: 12px; color: #bbb; }

.wish-card__actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
</style>
