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

      <div class="table-scroll-wrapper">
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

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="loadLogs"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'

const logs = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filterStatus = ref('pending')
const operating = ref(null)

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

onMounted(() => { loadLogs() })
</script>

<style scoped>
.task-approval { max-width: 1200px; }
.page-header { margin-bottom: 20px; }
.page-title { font-size: 22px; font-weight: 900; color: #333; margin: 0 0 6px; }
.page-subtitle { color: #999; margin: 0; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
.text-muted { color: #ccc; font-size: 13px; }
.table-scroll-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }
</style>
