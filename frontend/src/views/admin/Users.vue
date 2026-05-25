<template>
  <div class="admin-users">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增用户
          </el-button>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="keyword" placeholder="用户名/姓名" clearable @keyup.enter="loadUsers" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadUsers">查询</el-button>
        </el-form-item>
      </el-form>

      <div class="table-scroll-wrapper">
      <el-table :data="users" style="width: 100%" v-loading="loading">
        <el-table-column label="头像" width="70">
          <template #default="{ row }">
            <div class="table-avatar">
              <span v-if="!isUrl(row.avatar)" class="table-avatar-emoji">{{ getEmoji(row.avatar) }}</span>
              <el-avatar v-else :size="36" :src="row.avatar" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="110" />
        <el-table-column prop="real_name" label="姓名" width="100" />
        <el-table-column prop="email" label="邮箱" show-overflow-tooltip />
        <el-table-column prop="phone" label="电话" width="130" />
        <el-table-column prop="role" label="角色" width="130">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'" size="small">
              {{ row.role === 'admin' ? (row.is_super_admin ? '👑 超级管理员' : '管理员') : '普通用户' }}
            </el-tag>
            <el-tag v-if="row.is_child" type="warning" size="small" style="margin-left:4px;">🚀 宇航员</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_points" label="总积分" width="90" />
        <el-table-column prop="available_points" label="可用积分" width="90" />
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="账号状态" width="110">
          <template #default="{ row }">
            <el-tag
              :type="(row.status || 'active') === 'active' ? 'success' : 'warning'"
              size="small"
            >
              {{ (row.status || 'active') === 'active' ? '已激活' : '待审批' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="warning" @click="handleResetPassword(row)">重置密码</el-button>
            <el-button
              v-if="(row.status || 'active') === 'pending'"
              link
              type="success"
              @click="handleApprove(row)"
            >批准登舰</el-button>
          </template>
        </el-table-column>
      </el-table>
      </div>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        @current-change="loadUsers"
        class="pagination"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="520px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <!-- 头像选择区 -->
        <el-form-item label="头像">
          <div class="avatar-editor">
            <div class="avatar-preview">
              <span v-if="!isUrl(form.avatar)" class="preview-emoji">{{ getEmoji(form.avatar) }}</span>
              <el-avatar v-else :size="70" :src="form.avatar" />
            </div>
            <div class="avatar-right">
              <div class="preset-row">
                <div
                  v-for="p in presetAvatars"
                  :key="p.key"
                  class="preset-item"
                  :class="{ active: form.avatar === p.key }"
                  @click="form.avatar = p.key"
                >{{ p.emoji }}</div>
              </div>
              <el-upload
                :show-file-list="false"
                :before-upload="beforeUpload"
                :http-request="(opts) => uploadAvatarForForm(opts)"
                accept="image/jpeg,image/png,image/gif,image/webp"
              >
                <el-button size="small" plain round>
                  <el-icon><Upload /></el-icon> 上传图片
                </el-button>
              </el-upload>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" :placeholder="form.id ? '不修改请留空' : '请输入密码'" />
        </el-form-item>
        <el-form-item label="姓名" prop="real_name">
          <el-input v-model="form.real_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="角色" prop="role" v-if="userStore.isSuperAdmin()">
          <el-select v-model="form.role">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="超级管理员" v-if="form.role === 'admin' && userStore.isSuperAdmin()">
          <el-switch v-model="form.is_super_admin" />
          <span style="margin-left:10px;font-size:12px;color:#aaa;">超级管理员拥有全部权限</span>
        </el-form-item>

        <!-- 儿童账号配置（仅普通用户可设置） -->
        <template v-if="form.role === 'user'">
          <el-divider content-position="left"><span style="font-size:13px;color:#aaa;">🚀 宇航员专属通道</span></el-divider>
          <el-form-item label="儿童账号">
            <el-switch v-model="form.is_child" active-text="开启" inactive-text="关闭" />
            <span style="margin-left:10px;font-size:12px;color:#aaa;">开启后可在登录页宇航员通道选择该账号</span>
          </el-form-item>
          <el-form-item v-if="form.is_child" label="图案密码">
            <div class="pattern-editor">
              <div class="pattern-icons">
                <button
                  v-for="(icon, idx) in patternIcons"
                  :key="idx"
                  class="pattern-icon-btn"
                  :class="{ selected: form.child_pattern?.includes(idx), 'last-sel': form.child_pattern?.[form.child_pattern.length-1] === idx }"
                  type="button"
                  @click="togglePatternIcon(idx)"
                >
                  <span>{{ icon }}</span>
                  <span v-if="form.child_pattern?.includes(idx)" class="pattern-order">{{ form.child_pattern.indexOf(idx) + 1 }}</span>
                </button>
              </div>
              <div class="pattern-status">
                <span v-if="!form.child_pattern?.length" style="color:#bbb;">点击上方图标设置解锁顺序（需选满3个）</span>
                <span v-else-if="form.child_pattern.length < 3" style="color:#e6a23c;">已选 {{ form.child_pattern.length }} 个，还需 {{ 3 - form.child_pattern.length }} 个</span>
                <span v-else style="color:#67c23a;">✓ 密码已设置：{{ form.child_pattern.map(i => patternIcons[i]).join(' → ') }}</span>
                <el-button v-if="form.child_pattern?.length" link type="danger" size="small" @click="form.child_pattern = []">清除</el-button>
              </div>
            </div>
          </el-form-item>
        </template>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog v-model="resetPasswordDialogVisible" title="重置密码" width="400px">
      <el-form :model="resetPasswordForm" label-width="80px">
        <el-alert
          :title="`正在为用户 ${resetPasswordForm.username} 重置密码`"
          type="info"
          :closable="false"
          style="margin-bottom: 20px;"
        />
        <el-form-item label="新密码">
          <el-input
            v-model="resetPasswordForm.new_password"
            type="password"
            placeholder="请输入新密码（至少6位）"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input
            v-model="resetPasswordForm.confirm_password"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="resetPasswordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleResetPasswordSubmit" :loading="resetting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Upload } from '@element-plus/icons-vue'
import api from '@/utils/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const presetAvatars = [
  { key: 'preset_1', emoji: '🚀' },
  { key: 'preset_2', emoji: '👨‍🚀' },
  { key: 'preset_3', emoji: '🌟' },
  { key: 'preset_4', emoji: '🪐' },
  { key: 'preset_5', emoji: '🛸' },
  { key: 'preset_6', emoji: '⭐' },
]
const presetMap = Object.fromEntries(presetAvatars.map(p => [p.key, p.emoji]))

const isUrl = (v) => v && (v.startsWith('/') || v.startsWith('http'))
const getEmoji = (v) => (!v || isUrl(v)) ? '🚀' : (presetMap[v] || '🚀')

const users = ref([])
const loading = ref(false)
const keyword = ref('')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const resetPasswordDialogVisible = ref(false)
const resetting = ref(false)
const resetPasswordForm = reactive({
  user_id: null,
  username: '',
  new_password: '',
  confirm_password: ''
})
const formRef = ref(null)
const submitting = ref(false)

const form = reactive({
  id: null,
  username: '',
  password: '',
  real_name: '',
  email: '',
  phone: '',
  role: 'user',
  is_super_admin: false,
  avatar: 'preset_1',
  is_child: false,
  child_pattern: []
})

const patternIcons = ['🌟', '🚀', '🪐', '🛸', '👾', '🌙']

const togglePatternIcon = (idx) => {
  if (!form.child_pattern) form.child_pattern = []
  const pos = form.child_pattern.indexOf(idx)
  if (pos !== -1) {
    form.child_pattern.splice(pos, 1)
  } else if (form.child_pattern.length < 3) {
    form.child_pattern.push(idx)
  }
}

const rules = computed(() => ({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: form.id ? [] : [{ required: true, message: '请输入密码', trigger: 'blur' }],
  real_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
}))

const loadUsers = async () => {
  loading.value = true
  try {
    const res = await api.get('/users', {
      params: { page: page.value, per_page: pageSize.value, keyword: keyword.value }
    })
    users.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('加载用户失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增用户'
  Object.assign(form, { id: null, username: '', password: '', real_name: '', email: '', phone: '', role: 'user', is_super_admin: false, avatar: 'preset_1', is_child: false, child_pattern: [] })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑用户'
  Object.assign(form, {
    id: row.id,
    username: row.username,
    password: '',
    real_name: row.real_name,
    email: row.email,
    phone: row.phone,
    role: row.role,
    is_super_admin: row.is_super_admin || false,
    avatar: row.avatar || 'preset_1',
    is_child: row.is_child || false,
    child_pattern: row.child_pattern ? [...row.child_pattern] : []
  })
  dialogVisible.value = true
}

const beforeUpload = (file) => {
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片不能超过5MB')
    return false
  }
  return true
}

const uploadAvatarForForm = async ({ file }) => {
  const formData = new FormData()
  formData.append('file', file)
  try {
    const res = await api.post('/upload/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    form.avatar = res.data.url
    ElMessage.success('图片上传成功')
  } catch {
    ElMessage.error('图片上传失败')
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    if (form.is_child && (!form.child_pattern || form.child_pattern.length !== 3)) {
      ElMessage.error('请为儿童账号设置完整的3步图案密码')
      return
    }
    submitting.value = true
    try {
      if (form.id) {
        const payload = { ...form }
        if (!payload.password) delete payload.password
        await api.put(`/users/${form.id}`, payload)
        ElMessage.success('更新成功')
      } else {
        await api.post('/users', form)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      await loadUsers()
    } catch (error) {
      console.error('提交失败:', error)
    } finally {
      submitting.value = false
    }
  })
}

const handleResetPassword = (row) => {
  resetPasswordForm.user_id = row.id
  resetPasswordForm.username = row.real_name
  resetPasswordForm.new_password = ''
  resetPasswordForm.confirm_password = ''
  resetPasswordDialogVisible.value = true
}

const handleResetPasswordSubmit = async () => {
  if (!resetPasswordForm.new_password) { ElMessage.error('请输入新密码'); return }
  if (resetPasswordForm.new_password.length < 6) { ElMessage.error('密码长度至少6位'); return }
  if (resetPasswordForm.new_password !== resetPasswordForm.confirm_password) { ElMessage.error('两次输入的密码不一致'); return }
  resetting.value = true
  try {
    await api.post(`/users/${resetPasswordForm.user_id}/reset-password`, {
      new_password: resetPasswordForm.new_password
    })
    ElMessage.success('密码重置成功')
    resetPasswordDialogVisible.value = false
  } catch (error) {
    console.error('重置密码失败:', error)
  } finally {
    resetting.value = false
  }
}

onMounted(() => { loadUsers() })

const handleApprove = async (row) => {
  try {
    await api.put(`/users/${row.id}/status`, { status: 'active' })
    ElMessage.success(`${row.real_name} 已批准登舰！`)
    await loadUsers()
  } catch {
    ElMessage.error('操作失败，请重试')
  }
}
</script>

<style scoped>
.admin-users { max-width: 1400px; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form { margin-bottom: 20px; }

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 表格头像 */
.table-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B9D22, #7B68EE22);
  border: 2px solid #7B68EE33;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  overflow: hidden;
}
.table-avatar-emoji { line-height: 1; }

/* 弹窗头像编辑区 */
.avatar-editor {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.avatar-preview {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B9D22, #7B68EE22);
  border: 3px solid #7B68EE44;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  flex-shrink: 0;
  overflow: hidden;
}
.preview-emoji { line-height: 1; }

.avatar-right {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.preset-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.preset-item {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f5f0ff;
  border: 2px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.preset-item:hover { border-color: #7B68EE; transform: scale(1.1); }
.preset-item.active {
  border-color: #FF6B9D;
  background: #fff0f5;
  box-shadow: 0 0 0 3px rgba(255,107,157,0.2);
}

.table-scroll-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* 图案密码编辑器 */
.pattern-editor { display: flex; flex-direction: column; gap: 10px; width: 100%; }

.pattern-icons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  max-width: 240px;
}

.pattern-icon-btn {
  position: relative;
  height: 56px;
  background: #f5f0ff;
  border: 2px solid transparent;
  border-radius: 12px;
  font-size: 26px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}
.pattern-icon-btn:hover { border-color: #7B68EE; transform: scale(1.06); }
.pattern-icon-btn.selected {
  background: #f0e8ff;
  border-color: #FF6B9D;
  box-shadow: 0 0 0 2px rgba(255,107,157,0.2);
}

.pattern-order {
  position: absolute;
  top: 3px;
  right: 5px;
  font-size: 10px;
  font-weight: 900;
  color: #FF6B9D;
  background: rgba(255,107,157,0.15);
  border-radius: 50%;
  width: 15px;
  height: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pattern-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}
</style>
