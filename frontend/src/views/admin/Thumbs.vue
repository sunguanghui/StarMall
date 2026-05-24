<template>
  <div class="admin-thumbs">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>发放星辰币</span>
        </div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="130px" style="max-width: 620px;">
        <el-form-item label="选择用户" prop="user_id">
          <el-select
            v-model="form.user_id"
            filterable
            remote
            placeholder="请输入用户名搜索"
            :remote-method="searchUsers"
            :loading="searchLoading"
            style="width: 100%"
          >
            <el-option
              v-for="user in userOptions"
              :key="user.id"
              :label="`${user.real_name} (${user.username})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="操作模式">
          <el-switch
            v-model="form.is_deduction"
            active-text="宇宙惩罚（扣能量）"
            inactive-text="发放星辰币"
            active-color="#f56c6c"
            @change="onModeChange"
          />
        </el-form-item>

        <el-form-item v-if="!form.is_deduction" label="奖励类型" prop="thumb_type">
          <el-radio-group v-model="form.thumb_type">
            <el-radio label="single">
              <el-icon style="vertical-align: middle;"><Star /></el-icon>
              单星辰币 (+1 能量)
            </el-radio>
            <el-radio label="double">
              <el-icon style="vertical-align: middle;"><Promotion /></el-icon>
              双星辰币 (+5 能量)
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <template v-else>
          <el-form-item label="惩罚档位">
            <div class="punish-presets">
              <el-button
                v-for="p in punishPresets"
                :key="p.points"
                type="danger"
                :plain="form.deductionPoints !== p.points"
                round
                @click="selectPreset(p.points)"
              >
                {{ p.label }}
              </el-button>
            </div>
          </el-form-item>
          <el-form-item label="自定义黑洞">
            <div class="custom-punish">
              <el-input-number
                v-model="form.customPoints"
                :max="-1"
                :step="1"
                placeholder="输入负数"
                style="width:160px"
                @change="onCustomChange"
              />
              <span class="punish-unit">能量</span>
              <el-tag type="danger" v-if="currentDeduction !== null" class="punish-preview">
                ☄️ 本次将扣除 {{ Math.abs(currentDeduction) }} 点能量
              </el-tag>
            </div>
          </el-form-item>
        </template>

        <el-form-item label="原因" prop="reason">
          <el-input
            v-model="form.reason"
            type="textarea"
            :rows="3"
            :placeholder="form.is_deduction ? '请输入扣除能量的原因' : '请输入发放星辰币的原因'"
          />
        </el-form-item>

        <el-form-item label="舰长寄语（选填）">
          <el-input
            v-model="form.parent_message"
            type="textarea"
            :rows="2"
            placeholder="给孩子写一句温馨寄语，将显示在流水记录中"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            :type="form.is_deduction ? 'danger' : 'primary'"
            @click="handleSubmit"
            :loading="submitting"
          >
            {{ form.is_deduction ? `执行宇宙惩罚 (${currentDeduction ?? '?'} 能量)` : '发放星辰币' }}
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>最近发放记录</span>
        </div>
      </template>

      <el-table :data="records" style="width: 100%" v-loading="loading">
        <el-table-column prop="user_name" label="用户" width="120" />
        <el-table-column prop="thumb_type_name" label="类型" width="150" />
        <el-table-column label="能量" width="80">
          <template #default="{ row }">
            <span :class="{ 'negative-points': row.points < 0 }">{{ row.points }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="原因" show-overflow-tooltip />
        <el-table-column prop="parent_message" label="舰长寄语" show-overflow-tooltip />
        <el-table-column prop="given_by_name" label="赋能官 ✨" width="120" />
        <el-table-column prop="created_at" label="发放时间" width="180" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="isUndoable(row)"
              link
              type="danger"
              size="small"
              :loading="undoing === row.id"
              @click="handleUndo(row)"
            >后悔药</el-button>
          </template>
        </el-table-column>
      </el-table>

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
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Star, Promotion } from '@element-plus/icons-vue'
import api from '@/utils/api'

const formRef = ref(null)
const submitting = ref(false)
const searchLoading = ref(false)
const userOptions = ref([])
const undoing = ref(null)

const punishPresets = [
  { label: '陨石撞击 (-2)', points: -2 },
  { label: '星暴气流 (-5)', points: -5 },
  { label: '黑洞吞噬 (-10)', points: -10 },
]

const form = reactive({
  user_id: null,
  thumb_type: 'single',
  reason: '',
  parent_message: '',
  is_deduction: false,
  deductionPoints: null,
  customPoints: null
})

const currentDeduction = computed(() => {
  if (!form.is_deduction) return null
  if (form.customPoints !== null && form.customPoints <= -1) return form.customPoints
  return form.deductionPoints
})

const rules = {
  user_id: [{ required: true, message: '请选择用户', trigger: 'change' }],
  reason: [{ required: true, message: '请输入原因', trigger: 'blur' }]
}

const records = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const onModeChange = () => {
  form.deductionPoints = null
  form.customPoints = null
}

const selectPreset = (points) => {
  form.customPoints = null
  form.deductionPoints = form.deductionPoints === points ? null : points
}

const onCustomChange = (val) => {
  if (val !== null && val <= -1) {
    form.deductionPoints = null
  }
}

const searchUsers = async (query) => {
  if (!query) { userOptions.value = []; return }
  searchLoading.value = true
  try {
    const res = await api.get('/users', { params: { keyword: query, per_page: 20 } })
    userOptions.value = res.data.list.filter(u => u.role !== 'admin')
  } catch (error) {
    console.error('搜索用户失败:', error)
  } finally {
    searchLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  if (form.is_deduction && currentDeduction.value === null) {
    ElMessage.error('请选择惩罚档位或输入自定义扣分值')
    return
  }

  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      const payload = {
        user_id: form.user_id,
        thumb_type: form.is_deduction ? 'deduction' : form.thumb_type,
        reason: form.reason,
        parent_message: form.parent_message
      }
      if (form.is_deduction) {
        payload.points = currentDeduction.value
      }
      await api.post('/thumbs', payload)
      ElMessage.success(form.is_deduction ? `宇宙惩罚已执行（${currentDeduction.value} 能量）` : '星辰币发放成功')
      resetForm()
      await loadRecords()
    } catch (error) {
      console.error('操作失败:', error)
    } finally {
      submitting.value = false
    }
  })
}

const resetForm = () => {
  if (formRef.value) formRef.value.resetFields()
  form.user_id = null
  form.thumb_type = 'single'
  form.reason = ''
  form.parent_message = ''
  form.is_deduction = false
  form.deductionPoints = null
  form.customPoints = null
}

const isUndoable = (row) => {
  if (row.is_deleted) return false
  const created = new Date(row.created_at)
  return (Date.now() - created.getTime()) < 15 * 60 * 1000
}

const handleUndo = async (row) => {
  try {
    await ElMessageBox.confirm(
      `撤销对「${row.user_name}」的 ${row.points} 点能量操作？`,
      '后悔药',
      { confirmButtonText: '确认撤销', cancelButtonText: '取消', type: 'warning' }
    )
  } catch { return }
  undoing.value = row.id
  try {
    await api.post(`/thumbs/${row.id}/undo`)
    ElMessage.success('已撤销，能量已恢复')
    records.value = records.value.filter(r => r.id !== row.id)
  } catch (err) {
    ElMessage.error(err.response?.data?.message || '撤销失败')
  } finally {
    undoing.value = null
  }
}

const loadRecords = async () => {
  loading.value = true
  try {
    const res = await api.get('/thumbs', {
      params: { page: page.value, per_page: pageSize.value }
    })
    records.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('加载记录失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => { loadRecords() })
</script>

<style scoped>
.admin-thumbs {
  max-width: 1400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.negative-points {
  color: #f56c6c;
  font-weight: bold;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.punish-presets {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.custom-punish {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.punish-unit {
  font-size: 14px;
  color: #666;
}

.punish-preview {
  font-size: 13px;
  font-weight: 700;
}
</style>
