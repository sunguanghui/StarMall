<template>
  <div class="wishlist">
    <el-card class="form-card">
      <template #header>
        <span>✨ 提交新心愿</span>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="110px" style="max-width: 500px;">
        <el-form-item label="心愿名称" prop="title">
          <el-input v-model="form.title" placeholder="我想要的奖品名称" />
        </el-form-item>
        <el-form-item label="期望能量" prop="expected_points">
          <el-input-number v-model="form.expected_points" :min="1" />
          <span style="margin-left: 10px; font-size: 12px; color: #999;">当前可用能量：{{ userStore.userInfo.available_points }}</span>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">提交心愿</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <template #header>
        <span>我的心愿列表</span>
      </template>

      <el-table :data="wishlists" style="width: 100%" v-loading="loading">
        <el-table-column prop="title" label="心愿名称" show-overflow-tooltip />
        <el-table-column prop="expected_points" label="期望能量" width="110" />
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">{{ row.status_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="180" />
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const formRef = ref(null)
const submitting = ref(false)
const wishlists = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const form = reactive({ title: '', expected_points: 10 })

const rules = {
  title: [{ required: true, message: '请输入心愿名称', trigger: 'blur' }],
  expected_points: [{ required: true, message: '请输入期望能量', trigger: 'blur' }]
}

const statusTagType = (status) => {
  return { pending: 'warning', approved: 'success', rejected: 'info' }[status] || ''
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      await api.post('/wishlists', form)
      ElMessage.success('心愿提交成功，等待舰长审核 🚀')
      resetForm()
      await loadWishlists()
    } catch (error) {
      console.error('提交失败:', error)
    } finally {
      submitting.value = false
    }
  })
}

const resetForm = () => {
  if (formRef.value) formRef.value.resetFields()
  form.title = ''
  form.expected_points = 10
}

const loadWishlists = async () => {
  loading.value = true
  try {
    const res = await api.get('/wishlists', {
      params: { page: page.value, per_page: pageSize.value }
    })
    wishlists.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('加载心愿列表失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadWishlists()
})
</script>

<style scoped>
.wishlist {
  max-width: 1000px;
}

.form-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
