<template>
  <div class="task-approval">
    <div class="page-header">
      <h2 class="page-title">✅ 任务核验舱</h2>
      <p class="page-subtitle">审核宇航员提交的任务打卡，批准后自动注入能量</p>
    </div>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>打卡审核队列</span>
          <el-select v-model="filterStatus" size="small" style="width:120px" @change="loadLogs">
            <el-option label="待核验" value="pending" />
            <el-option label="已注入" value="approved" />
            <el-option label="已驳回" value="rejected" />
            <el-option label="全部" value="" />
          </el-select>
        </div>
      </template>

      <!-- ===== PC 端表格（> 768px） ===== -->
      <div class="table-scroll-wrapper pc-table-view">
        <el-table :data="logs" v-loading="loading" style="width:100%">
          <el-table-column prop="user_name" label="宇航员" width="100" />
          <el-table-column prop="task_title" label="任务名称" min-width="150" show-overflow-tooltip />
          <el-table-column prop="task_type" label="类型" width="120">
            <template #default="{ row }">
              <el-tag :type="row.task_type === 'daily' ? 'primary' : 'warning'" size="small">
                {{ row.task_type === 'daily' ? '📅 每日日常' : '🏆 阶段里程碑' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="energy_reward" label="奖励能量" width="100">
            <template #default="{ row }">+{{ row.energy_reward }} ⚡</template>
          </el-table-column>
          <el-table-column prop="reviewer_name" label="负责赋能官" width="110">
            <template #default="{ row }">
              <span v-if="row.reviewer_name">{{ row.reviewer_name }}</span>
              <span v-else class="text-muted">全体领航员</span>
            </template>
          </el-table-column>
          <el-table-column prop="status_name" label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="statusTagType(row.status)" size="small">{{ row.status_name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="提交时间" width="160" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="{ row }">
              <template v-if="row.status === 'pending'">
                <el-button link type="success" @click="handleApprove(row)" :loading="operating === row.id">⚡ 能量注入</el-button>
                <el-button link type="danger" @click="handleReject(row)" :loading="operating === row.id">🔄 驳回重试</el-button>
              </template>
              <span v-else class="text-muted">已处理</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- ===== 移动端卡片列表（≤ 768px） ===== -->
      <div class="mobile-card-view mobile-card-list" v-loading="loading">
        <div
          v-for="row in logs"
          :key="row.id"
          class="approval-card"
          :class="{
            'approval-card--pending':  row.status === 'pending',
            'approval-card--approved': row.status === 'approved',
            'approval-card--rejected': row.status === 'rejected'
          }"
        >
          <!-- 顶部：宇航员 + 任务名 + 状态标签 -->
          <div class="approval-card__top">
            <div class="approval-card__info">
              <span class="approval-card__user">🧑‍🚀 {{ row.user_name }}</span>
              <span class="approval-card__title">{{ row.task_title }}</span>
            </div>
            <el-tag :type="statusTagType(row.status)" size="small" class="approval-card__status">
              {{ row.status_name }}
            </el-tag>
          </div>

          <!-- 中部：类型、奖励能量、负责赋能官 -->
          <div class="approval-card__meta">
            <el-tag :type="row.task_type === 'daily' ? 'primary' : 'warning'" size="small">
              {{ row.task_type === 'daily' ? '📅 每日日常' : '🏆 阶段里程碑' }}
            </el-tag>
            <span class="approval-card__energy">+{{ row.energy_reward }} ⚡</span>
            <span class="approval-card__reviewer">
              {{ row.reviewer_name || '全体领航员' }}
            </span>
          </div>

          <!-- 提交时间 -->
          <div class="approval-card__time">🕐 {{ row.created_at }}</div>

          <!-- 底部操作按钮 -->
          <div class="approval-card__actions">
            <template v-if="row.status === 'pending'">
              <el-button
                type="success"
                size="small"
                :loading="operating === row.id"
                @click="handleApprove(row)"
              >⚡ 能量注入</el-button>
              <el-button
                type="danger"
                size="small"
                plain
                :loading="operating === row.id"
                @click="handleReject(row)"
              >🔄 驳回重试</el-button>
            </template>
            <span v-else class="text-muted">已处理</span>
          </div>
        </div>
        <el-empty v-if="!loading && logs.length === 0" description="暂无审核记录" />
      </div>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :layout="isMobile ? 'prev, pager, next' : 'total, prev, pager, next'"
        @current-change="loadLogs"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'

const logs = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterStatus = ref('pending')
const operating = ref(null)

const isMobile = ref(window.innerWidth <= 768)
const handleResize = () => { isMobile.value = window.innerWidth <= 768 }

const statusTagType = (status) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warning'
}

const loadLogs = async () => {
  loading.value = true
  try {
    const params = { page: page.value, per_page: pageSize.value }
    if (filterStatus.value) params.status = filterStatus.value
    const res = await api.get('/task-logs', { params })
    logs.value = res.data?.list || []
    total.value = res.data?.total || 0
  } catch { ElMessage.error('加载记录失败') }
  finally { loading.value = false }
}

const handleApprove = async (row) => {
  operating.value = row.id
  try {
    await api.post(`/task-logs/${row.id}/approve`)
    ElMessage.success(`⚡ 能量注入成功！已为 ${row.user_name} 发放 ${row.energy_reward} 点能量`)
    await loadLogs()
  } catch (err) { ElMessage.error(err.response?.data?.message || '操作失败') }
  finally { operating.value = null }
}

const handleReject = async (row) => {
  try {
    await ElMessageBox.confirm(`确定驳回 ${row.user_name} 的「${row.task_title}」打卡？`, '驳回重试', { type: 'warning' })
    operating.value = row.id
    await api.post(`/task-logs/${row.id}/reject`)
    ElMessage.success('已驳回，宇航员可重新提交')
    await loadLogs()
  } catch {}
  finally { operating.value = null }
}

onMounted(() => {
  loadLogs()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.task-approval { max-width: 1200px; }
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

/* ===== 移动端审核卡片 ===== */
.mobile-card-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 60px;
}

.approval-card {
  border-radius: 16px;
  padding: 14px 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1.5px solid #e8e0f8;
  background: linear-gradient(135deg, #faf8ff 0%, #fff9f0 100%);
  box-shadow: 0 2px 10px rgba(123, 104, 238, 0.07);
}

.approval-card--pending {
  border-color: #f0c060;
  background: linear-gradient(135deg, #fffdf0 0%, #fff8e0 100%);
}

.approval-card--approved {
  border-color: #a0dba0;
  background: linear-gradient(135deg, #f0fff4 0%, #e8f8e8 100%);
}

.approval-card--rejected {
  border-color: #f0a0a0;
  background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
}

.approval-card__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.approval-card__info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.approval-card__user {
  font-size: 15px;
  font-weight: 700;
  color: #333;
}

.approval-card__title {
  font-size: 13px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.approval-card__status {
  flex-shrink: 0;
}

.approval-card__meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.approval-card__energy {
  font-size: 16px;
  font-weight: 900;
  color: #FF6B9D;
}

.approval-card__reviewer {
  font-size: 12px;
  color: #999;
}

.approval-card__time {
  font-size: 12px;
  color: #bbb;
}

.approval-card__actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 6px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}
</style>
