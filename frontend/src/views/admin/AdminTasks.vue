<template>
  <div class="admin-tasks">
    <div class="page-header">
      <h2 class="page-title">🎯 星际任务定义管理</h2>
      <p class="page-subtitle">创建和管理宇航员可执行的星际任务蓝图（审核探索日志请前往「任务核验舱」）</p>
    </div>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>星际任务蓝图列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon> 创建任务
          </el-button>
        </div>
      </template>

      <!-- ===== PC 端表格（> 768px） ===== -->
      <div class="desktop-only-wrapper">
        <div class="table-scroll-wrapper">
          <el-table :data="tasks" v-loading="tasksLoading" style="width:100%">
            <el-table-column prop="title" label="星际任务名称" min-width="160" show-overflow-tooltip />
            <el-table-column prop="type_name" label="任务类型" width="120">
              <template #default="{ row }">
                <el-tag :type="row.type === 'daily' ? 'primary' : 'warning'" size="small">{{ row.type_name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="energy_reward" label="注入能量" width="100">
              <template #default="{ row }">+{{ row.energy_reward }} ⚡</template>
            </el-table-column>
            <el-table-column prop="reviewer_name" label="专属赋能官" width="120">
              <template #default="{ row }">
                <span v-if="row.reviewer_name">{{ row.reviewer_name }}</span>
                <span v-else class="text-muted">全体领航员</span>
              </template>
            </el-table-column>
            <el-table-column prop="is_active" label="任务状态" width="90">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'" size="small">{{ row.is_active ? '已启用' : '已停用' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="160" />
            <el-table-column label="指令" width="160" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" @click="handleEdit(row)">重新校准</el-button>
                <el-button link :type="row.is_active ? 'danger' : 'success'" @click="handleToggle(row)">
                  {{ row.is_active ? '停用' : '启用' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- ===== 移动端卡片列表（≤ 768px） ===== -->
      <div class="mobile-only-wrapper">
        <div class="mobile-card-list" v-loading="tasksLoading">
          <div
            v-for="row in tasks"
            :key="row.id"
            class="task-card"
            :class="{ 'task-card--inactive': !row.is_active }"
          >
            <!-- 顶部：任务名 + 启用状态标签 -->
            <div class="task-card__top">
              <div class="task-card__title-wrap">
                <span class="task-card__title">{{ row.title }}</span>
              </div>
              <el-tag :type="row.is_active ? 'success' : 'info'" size="small" class="task-card__status">
                {{ row.is_active ? '已启用' : '已停用' }}
              </el-tag>
            </div>

            <!-- 中部：类型、注入能量、专属赋能官 -->
            <div class="task-card__meta">
              <div class="task-card__meta-item">
                <span class="meta-label">任务类型</span>
                <el-tag :type="row.type === 'daily' ? 'primary' : 'warning'" size="small">
                  {{ row.type_name }}
                </el-tag>
              </div>
              <div class="task-card__meta-item">
                <span class="meta-label">注入能量</span>
                <span class="meta-value energy">+{{ row.energy_reward }} ⚡</span>
              </div>
              <div class="task-card__meta-item">
                <span class="meta-label">赋能官</span>
                <span class="meta-value">{{ row.reviewer_name || '全体领航员' }}</span>
              </div>
            </div>

            <!-- 底部：创建时间 + 操作按钮 -->
            <div class="task-card__footer">
              <span class="task-card__time">🕐 {{ row.created_at }}</span>
              <div class="task-card__actions">
                <el-button
                  size="small"
                  type="primary"
                  plain
                  @click="handleEdit(row)"
                >重新校准</el-button>
                <el-button
                  size="small"
                  :type="row.is_active ? 'danger' : 'success'"
                  plain
                  @click="handleToggle(row)"
                >{{ row.is_active ? '停用' : '启用' }}</el-button>
              </div>
            </div>
          </div>
          <el-empty v-if="!tasksLoading && tasks.length === 0" description="暂无星际任务蓝图" />
        </div>
      </div>
    </el-card>

    <!-- 创建/校准任务对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" :width="dialogWidth">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="任务名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入星际任务名称" />
        </el-form-item>
        <el-form-item label="任务类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio value="daily">📅 每日探索</el-radio>
            <el-radio value="milestone">🏆 阶段里程碑</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="注入能量" prop="energy_reward">
          <el-input-number v-model="form.energy_reward" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="专属赋能官" v-if="userStore.isSuperAdmin()">
          <el-select v-model="form.reviewer_id" clearable placeholder="不选则全体领航员均可核验" style="width:100%">
            <el-option
              v-for="admin in adminOptions"
              :key="admin.id"
              :label="admin.real_name + (admin.is_super_admin ? ' 👑' : '')"
              :value="admin.id"
            />
          </el-select>
          <div class="form-tip">若不选择，则所有领航员均可核验探索日志</div>
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import api from '@/utils/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const tasks = ref([])
const tasksLoading = ref(false)
const adminOptions = ref([])

const dialogVisible = ref(false)
const isMobile = ref(window.innerWidth <= 768)
const handleResize = () => { isMobile.value = window.innerWidth <= 768 }
const dialogWidth = computed(() => isMobile.value ? '92%' : '480px')
const dialogTitle = ref('创建星际任务')
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({ id: null, title: '', type: 'daily', energy_reward: 1, is_active: true, reviewer_id: null })
const rules = {
  title: [{ required: true, message: '请输入星际任务名称', trigger: 'blur' }],
  type: [{ required: true }],
  energy_reward: [{ required: true }]
}

const loadTasks = async () => {
  tasksLoading.value = true
  try {
    const res = await api.get('/tasks', { params: { include_inactive: true } })
    tasks.value = res.data || []
  } catch { ElMessage.error('加载星际任务失败') }
  finally { tasksLoading.value = false }
}

const loadAdmins = async () => {
  try {
    const res = await api.get('/admins')
    adminOptions.value = res.data
  } catch {}
}

const handleAdd = () => {
  dialogTitle.value = '创建星际任务'
  Object.assign(form, { id: null, title: '', type: 'daily', energy_reward: 1, is_active: true, reviewer_id: null })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '重新校准任务参数'
  Object.assign(form, {
    id: row.id,
    title: row.title,
    type: row.type,
    energy_reward: row.energy_reward,
    is_active: row.is_active,
    reviewer_id: row.reviewer_id || null
  })
  dialogVisible.value = true
}

const handleToggle = async (row) => {
  try {
    await api.put(`/tasks/${row.id}`, { is_active: !row.is_active })
    ElMessage.success(row.is_active ? '星际任务已停用' : '星际任务已启用')
    await loadTasks()
  } catch (err) { ElMessage.error(err.response?.data?.message || '操作失败') }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      const payload = { ...form }
      if (!userStore.isSuperAdmin()) delete payload.reviewer_id
      if (form.id) {
        await api.put(`/tasks/${form.id}`, payload)
        ElMessage.success('任务参数校准成功')
      } else {
        await api.post('/tasks', payload)
        ElMessage.success('星际任务创建成功')
      }
      dialogVisible.value = false
      await loadTasks()
    } catch (err) { ElMessage.error(err.response?.data?.message || '提交失败') }
    finally { submitting.value = false }
  })
}

onMounted(() => {
  loadTasks()
  if (userStore.isSuperAdmin()) loadAdmins()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.admin-tasks { max-width: 1200px; }
.page-header { margin-bottom: 20px; }
.page-title { font-size: 22px; font-weight: 900; color: #333; margin: 0 0 6px; }
.page-subtitle { color: #999; margin: 0; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.text-muted { color: #ccc; font-size: 13px; }
.form-tip { font-size: 12px; color: #aaa; margin-top: 4px; }
.table-scroll-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }

@media (max-width: 768px) {
  :deep(.el-dialog) {
    margin: 8px auto !important;
    border-radius: 18px !important;
  }

  :deep(.el-dialog__body) {
    padding: 16px 14px !important;
  }
}

/* ===== 移动端任务卡片 ===== */
.mobile-card-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 60px;
}

.task-card {
  border-radius: 16px;
  padding: 14px 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1.5px solid #d0e8ff;
  background: linear-gradient(135deg, #f5faff 0%, #f0f8ff 100%);
  box-shadow: 0 2px 10px rgba(65, 88, 208, 0.07);
}

.task-card--inactive {
  border-color: #ddd;
  background: linear-gradient(135deg, #f8f8f8 0%, #f2f2f2 100%);
  opacity: 0.7;
}

.task-card__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.task-card__title-wrap {
  flex: 1;
  min-width: 0;
}

.task-card__title {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  word-break: break-word;
}

.task-card__status {
  flex-shrink: 0;
}

.task-card__meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.task-card__meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
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
  font-size: 17px;
  font-weight: 900;
  color: #FF6B9D;
}

.task-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding-top: 8px;
}

.task-card__time {
  font-size: 12px;
  color: #bbb;
}

.task-card__actions {
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
