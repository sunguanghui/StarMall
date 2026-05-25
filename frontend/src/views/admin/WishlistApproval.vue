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

      <!-- ===== PC 端表格（> 768px） ===== -->
      <div class="desktop-only-wrapper">
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
      </div>

      <!-- ===== 移动端卡片列表（≤ 768px） ===== -->
      <div class="mobile-only-wrapper">
        <div class="mobile-card-list" v-loading="loading">
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
            <!-- 顶部：心愿名称 + 状态标签 -->
            <div class="wish-card__top">
              <div class="wish-card__title-wrap">
                <span class="wish-card__icon">💫</span>
                <span class="wish-card__title">{{ row.title }}</span>
              </div>
              <el-tag :type="statusTagType(row.status)" size="small" class="wish-card__status">
                {{ row.status_name }}
              </el-tag>
            </div>

            <!-- 中部：宇航员 + 期望能量 -->
            <div class="wish-card__meta">
              <div class="wish-card__meta-item">
                <span class="meta-label">申请人</span>
                <span class="meta-value">🧑‍🚀 {{ row.user_name }}</span>
              </div>
              <div class="wish-card__meta-item">
                <span class="meta-label">期望能量</span>
                <span class="meta-value energy">{{ row.expected_points }} ⚡</span>
              </div>
            </div>

            <!-- 提交时间 + 操作按钮 -->
            <div class="wish-card__footer">
              <span class="wish-card__time">🕐 {{ row.created_at }}</span>
              <div class="wish-card__actions">
                <template v-if="row.status === 'pending'">
                  <el-button
                    type="success"
                    size="small"
                    @click="handleApprove(row)"
                  >🔬 批准研发</el-button>
                  <el-button
                    type="danger"
                    size="small"
                    plain
                    @click="handleReject(row)"
                  >❌ 驳回</el-button>
                </template>
                <span v-else class="text-muted">已处理</span>
              </div>
            </div>
          </div>
          <el-empty v-if="!loading && wishlists.length === 0" description="暂无心愿蓝图" />
        </div>
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
const filterStatus = ref('pending')
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

onMounted(() => {
  loadWishlists()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.wishlist-approval { max-width: 1200px; }
.page-header { margin-bottom: 20px; }
.page-title { font-size: 22px; font-weight: 900; color: #333; margin: 0 0 6px; }
.page-subtitle { color: #999; margin: 0; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.text-muted { color: #ccc; font-size: 13px; }
.table-scroll-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .pagination {
    justify-content: center;
    flex-wrap: wrap;
  }
}

/* ===== 移动端心愿蓝图卡片 ===== */
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
  border: 1.5px solid #e8e0f8;
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
  opacity: 0.75;
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

.wish-card__icon {
  font-size: 20px;
  flex-shrink: 0;
}

.wish-card__title {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.wish-card__status {
  flex-shrink: 0;
}

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

.wish-card__time {
  font-size: 12px;
  color: #bbb;
}

.wish-card__actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

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
