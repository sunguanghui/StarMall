<template>
  <div class="admin-tasks">
    <div class="page-header">
      <h2 class="page-title">🎯 任务定义管理</h2>
      <p class="page-subtitle">创建和管理宇航员可执行的任务蓝图（审核打卡请前往「任务核验舱」）</p>
    </div>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务蓝图列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon> 新增任务
          </el-button>
        </div>
      </template>

      <div class="table-scroll-wrapper">
        <el-table :data="tasks" v-loading="tasksLoading" style="width:100%">
          <el-table-column prop="title" label="任务名称" min-width="160" show-overflow-tooltip />
          <el-table-column prop="type_name" label="类型" width="120">
            <template #default="{ row }">
              <el-tag :type="row.type === 'daily' ? 'primary' : 'warning'" size="small">{{ row.type_name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="energy_reward" label="奖励能量" width="100">
            <template #default="{ row }">+{{ row.energy_reward }} ⚡</template>
          </el-table-column>
          <el-table-column prop="reviewer_name" label="专属赋能官" width="120">
            <template #default="{ row }">
              <span v-if="row.reviewer_name">{{ row.reviewer_name }}</span>
              <span v-else class="text-muted">全体领航员</span>
            </template>
          </el-table-column>
          <el-table-column prop="is_active" label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'info'" size="small">{{ row.is_active ? '已启用' : '已停用' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="160" />
          <el-table-column label="操作" width="160" fixed="right">
            <template #default="{ row }">
              <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
              <el-button link :type="row.is_active ? 'danger' : 'success'" @click="handleToggle(row)">
                {{ row.is_active ? '停用' : '启用' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 新增/编辑任务对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="480px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="任务名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="任务类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio value="daily">📅 每日日常</el-radio>
            <el-radio value="milestone">🏆 阶段里程碑</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="奖励能量" prop="energy_reward">
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
          <div class="form-tip">若不选择，则所有领航员均可核验</div>
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import api from '@/utils/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const tasks = ref([])
const tasksLoading = ref(false)
const adminOptions = ref([])

const dialogVisible = ref(false)
const dialogTitle = ref('新增任务')
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({ id: null, title: '', type: 'daily', energy_reward: 1, is_active: true, reviewer_id: null })
const rules = {
  title: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  type: [{ required: true }],
  energy_reward: [{ required: true }]
}

const loadTasks = async () => {
  tasksLoading.value = true
  try {
    const res = await api.get('/tasks', { params: { include_inactive: true } })
    tasks.value = res.data || []
  } catch { ElMessage.error('加载任务失败') }
  finally { tasksLoading.value = false }
}

const loadAdmins = async () => {
  try {
    const res = await api.get('/admins')
    adminOptions.value = res.data.data
  } catch {}
}

const handleAdd = () => {
  dialogTitle.value = '新增任务'
  Object.assign(form, { id: null, title: '', type: 'daily', energy_reward: 1, is_active: true, reviewer_id: null })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑任务'
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
    ElMessage.success(row.is_active ? '任务已停用' : '任务已启用')
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
        ElMessage.success('更新成功')
      } else {
        await api.post('/tasks', payload)
        ElMessage.success('创建成功')
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
</style>
