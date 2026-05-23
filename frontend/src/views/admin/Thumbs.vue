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

        <el-form-item label="扣除能量模式">
          <el-switch
            v-model="form.is_deduction"
            active-text="红牌警告（扣1能量）"
            inactive-text="发放星辰币"
            active-color="#f56c6c"
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

        <el-form-item v-else label="扣除说明">
          <el-tag type="danger">本次将扣除该用户 1 点能量</el-tag>
        </el-form-item>

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
            {{ form.is_deduction ? '执行红牌警告' : '发放星辰币' }}
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
        <el-table-column prop="given_by_name" label="发放人" width="120" />
        <el-table-column prop="created_at" label="发放时间" width="180" />
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, Promotion } from '@element-plus/icons-vue'
import api from '@/utils/api'

const formRef = ref(null)
const submitting = ref(false)
const searchLoading = ref(false)
const userOptions = ref([])

const form = reactive({
  user_id: null,
  thumb_type: 'single',
  reason: '',
  parent_message: '',
  is_deduction: false
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

const searchUsers = async (query) => {
  if (!query) {
    userOptions.value = []
    return
  }
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
      await api.post('/thumbs', payload)
      ElMessage.success(form.is_deduction ? '红牌警告已执行' : '星辰币发放成功')
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

onMounted(() => {
  loadRecords()
})
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
</style>
