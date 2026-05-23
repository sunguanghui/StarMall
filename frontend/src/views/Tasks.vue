<template>
  <div class="tasks-page">
    <div class="page-header">
      <h2 class="page-title">🎯 任务大厅</h2>
      <p class="page-subtitle">完成任务获取能量，助力星际之旅</p>
    </div>

    <el-tabs v-model="activeTab" class="task-tabs">
      <el-tab-pane label="📅 每日日常" name="daily">
        <div v-loading="loading" class="task-grid">
          <div v-for="task in dailyTasks" :key="task.id" class="task-card" :class="getCardClass(task)">
            <div class="task-card-inner">
              <div class="task-icon">📋</div>
              <div class="task-info">
                <div class="task-title">{{ task.title }}</div>
                <div class="task-reward">
                  <span class="reward-label">奖励</span>
                  <span class="reward-value">+{{ task.energy_reward }} ⚡</span>
                </div>
              </div>
              <div class="task-action">
                <el-button
                  v-if="!task.today_log"
                  type="primary"
                  round
                  size="small"
                  @click="submitTask(task)"
                  :loading="submitting === task.id"
                >打卡</el-button>
                <el-tag v-else-if="task.today_log.status === 'pending'" type="warning" round size="small">审核中</el-tag>
                <el-tag v-else-if="task.today_log.status === 'approved'" type="success" round size="small">✅ 已完成</el-tag>
                <el-tag v-else type="danger" round size="small">已驳回</el-tag>
              </div>
            </div>
          </div>
          <div v-if="!loading && dailyTasks.length === 0" class="empty-tip">暂无每日任务</div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="🏆 阶段里程碑" name="milestone">
        <div v-loading="loading" class="task-grid">
          <div v-for="task in milestoneTasks" :key="task.id" class="task-card milestone" :class="getCardClass(task)">
            <div class="task-card-inner">
              <div class="task-icon">🏆</div>
              <div class="task-info">
                <div class="task-title">{{ task.title }}</div>
                <div class="task-reward">
                  <span class="reward-label">奖励</span>
                  <span class="reward-value">+{{ task.energy_reward }} ⚡</span>
                </div>
              </div>
              <div class="task-action">
                <el-button
                  v-if="!task.today_log"
                  type="warning"
                  round
                  size="small"
                  @click="submitTask(task)"
                  :loading="submitting === task.id"
                >申请</el-button>
                <el-tag v-else-if="task.today_log.status === 'pending'" type="warning" round size="small">审核中</el-tag>
                <el-tag v-else-if="task.today_log.status === 'approved'" type="success" round size="small">✅ 已完成</el-tag>
                <el-tag v-else type="danger" round size="small">已驳回</el-tag>
              </div>
            </div>
          </div>
          <div v-if="!loading && milestoneTasks.length === 0" class="empty-tip">暂无里程碑任务</div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="📜 我的记录" name="logs">
        <el-table :data="myLogs" v-loading="logsLoading" style="width:100%">
          <el-table-column prop="task_title" label="任务名称" min-width="140" show-overflow-tooltip />
          <el-table-column prop="task_type" label="类型" width="110">
            <template #default="{ row }">
              <el-tag :type="row.task_type === 'daily' ? 'primary' : 'warning'" size="small">
                {{ row.task_type === 'daily' ? '每日日常' : '阶段里程碑' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="energy_reward" label="奖励能量" width="90">
            <template #default="{ row }">+{{ row.energy_reward }} ⚡</template>
          </el-table-column>
          <el-table-column prop="status_name" label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="statusTagType(row.status)" size="small">{{ row.status_name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="提交时间" width="160" />
        </el-table>
        <el-pagination
          v-if="logsTotal > 0"
          v-model:current-page="logsPage"
          v-model:page-size="logsPageSize"
          :total="logsTotal"
          layout="total, prev, pager, next"
          @current-change="loadMyLogs"
          class="pagination"
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'

const activeTab = ref('daily')
const loading = ref(false)
const tasks = ref([])
const submitting = ref(null)

const logsLoading = ref(false)
const myLogs = ref([])
const logsPage = ref(1)
const logsPageSize = ref(20)
const logsTotal = ref(0)

const dailyTasks = computed(() => tasks.value.filter(t => t.type === 'daily'))
const milestoneTasks = computed(() => tasks.value.filter(t => t.type === 'milestone'))

const getCardClass = (task) => {
  if (!task.today_log) return ''
  if (task.today_log.status === 'approved') return 'done'
  if (task.today_log.status === 'pending') return 'pending'
  if (task.today_log.status === 'rejected') return 'rejected'
  return ''
}

const statusTagType = (status) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warning'
}

const loadTasks = async () => {
  loading.value = true
  try {
    const res = await api.get('/tasks')
    tasks.value = res.data.data
  } catch {
    ElMessage.error('加载任务失败')
  } finally {
    loading.value = false
  }
}

const loadMyLogs = async () => {
  logsLoading.value = true
  try {
    const res = await api.get('/task-logs', { params: { page: logsPage.value, per_page: logsPageSize.value } })
    myLogs.value = res.data.data.list
    logsTotal.value = res.data.data.total
  } catch {
    ElMessage.error('加载记录失败')
  } finally {
    logsLoading.value = false
  }
}

const submitTask = async (task) => {
  submitting.value = task.id
  try {
    await api.post('/task-logs', { task_id: task.id })
    ElMessage.success('打卡成功，等待舰长审核 🎉')
    await loadTasks()
  } catch (err) {
    ElMessage.error(err.response?.data?.message || '提交失败')
  } finally {
    submitting.value = null
  }
}

watch(activeTab, (tab) => {
  if (tab === 'logs') loadMyLogs()
})

onMounted(() => { loadTasks() })
</script>

<style scoped>
.tasks-page { max-width: 900px; }

.page-header { margin-bottom: 24px; }
.page-title { font-size: 24px; font-weight: 900; color: #333; margin: 0 0 6px; }
.page-subtitle { color: #999; margin: 0; font-size: 14px; }

.task-tabs :deep(.el-tabs__nav-wrap::after) { height: 1px; background: #f0e8ff; }
.task-tabs :deep(.el-tabs__item) { font-size: 15px; font-weight: 600; }
.task-tabs :deep(.el-tabs__item.is-active) { color: #7B68EE; }
.task-tabs :deep(.el-tabs__active-bar) { background-color: #7B68EE; }

.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  padding: 16px 0;
}

.task-card {
  border-radius: 16px;
  background: white;
  border: 2px solid #f0e8ff;
  transition: all 0.25s ease;
  overflow: hidden;
}
.task-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(123,104,238,0.15); }
.task-card.done { border-color: #67c23a44; background: #f0fff0; }
.task-card.pending { border-color: #e6a23c44; background: #fffbf0; }
.task-card.rejected { border-color: #f56c6c44; background: #fff5f5; opacity: 0.75; }
.task-card.milestone { border-color: #ffd70044; }

.task-card-inner {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 16px;
}

.task-icon { font-size: 28px; flex-shrink: 0; }

.task-info { flex: 1; min-width: 0; }
.task-title { font-size: 15px; font-weight: 700; color: #333; margin-bottom: 6px; }
.task-reward { display: flex; align-items: center; gap: 6px; }
.reward-label { font-size: 12px; color: #999; }
.reward-value { font-size: 13px; font-weight: 700; color: #FF6B9D; }

.task-action { flex-shrink: 0; }

.empty-tip { color: #ccc; text-align: center; padding: 40px; grid-column: 1 / -1; font-size: 15px; }

.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
