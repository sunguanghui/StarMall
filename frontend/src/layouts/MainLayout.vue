<template>
  <el-container class="main-container">
    <!-- 桌面侧边栏 -->
    <el-aside width="200px" class="sidebar desktop-sidebar">
      <div class="logo">
        <h2>🚀 星途补给站</h2>
      </div>
      <el-menu :default-active="activeMenu" router class="menu">

        <!-- 宇航员菜单 -->
        <template v-if="!userStore.isAdmin()">
          <el-menu-item index="/dashboard"><el-icon><House /></el-icon><span>空间站控制台</span></el-menu-item>
          <el-menu-item index="/mall"><el-icon><Shop /></el-icon><span>能量补给舱</span></el-menu-item>
          <el-menu-item index="/my-points"><el-icon><TrophyBase /></el-icon><span>航行能量轨迹</span></el-menu-item>
          <el-menu-item index="/my-exchanges"><el-icon><ShoppingCart /></el-icon><span>兑换发货舱</span></el-menu-item>
          <el-menu-item index="/tasks"><el-icon><Aim /></el-icon><span>星际任务雷达</span></el-menu-item>
          <el-menu-item index="/wishlist"><el-icon><Star /></el-icon><span>许愿发射台</span></el-menu-item>
          <el-menu-item index="/help"><el-icon><QuestionFilled /></el-icon><span>星际航行指南</span></el-menu-item>
        </template>

        <!-- 舰长/领航员菜单 -->
        <template v-else>
          <el-menu-item index="/admin/dashboard"><el-icon><DataAnalysis /></el-icon><span>舰队指挥中心</span></el-menu-item>
          <el-menu-item index="/admin/thumbs"><el-icon><Lightning /></el-icon><span>能量源控制</span></el-menu-item>
          <el-menu-item index="/admin/task-approval"><el-icon><Checked /></el-icon><span>任务核验舱</span></el-menu-item>
          <el-menu-item index="/admin/exchange-delivery"><el-icon><Box /></el-icon><span>补给调度室</span></el-menu-item>
          <el-menu-item index="/admin/wishlist-approval"><el-icon><Compass /></el-icon><span>蓝图解析室</span></el-menu-item>
          <el-menu-item index="/admin/tasks"><el-icon><Aim /></el-icon><span>任务定义管理</span></el-menu-item>
          <template v-if="userStore.isSuperAdmin()">
            <el-menu-item index="/admin/users"><el-icon><UserFilled /></el-icon><span>乘员编制管理</span></el-menu-item>
            <el-menu-item index="/admin/products"><el-icon><Shop /></el-icon><span>补给物资库房</span></el-menu-item>
            <el-menu-item index="/admin/exchanges"><el-icon><List /></el-icon><span>全站星际日志</span></el-menu-item>
            <el-menu-item index="/admin/broadcast-settings"><el-icon><Mic /></el-icon><span>星际广播台</span></el-menu-item>
          </template>
        </template>

      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <el-button class="hamburger-btn" @click="drawerVisible = true" text>
          <el-icon :size="24"><Fold /></el-icon>
        </el-button>
        <div class="header-right">
          <el-tag v-if="userStore.isSuperAdmin()" type="danger" size="small" round class="role-tag">👑 舰长</el-tag>
          <el-tag v-else-if="userStore.isAdmin()" type="warning" size="small" round class="role-tag">🧭 领航员</el-tag>
          <span class="username">{{ userStore.userInfo?.real_name }}</span>
          <el-dropdown @command="handleCommand">
            <div class="avatar-wrap">
              <span v-if="!avatarIsUrl" class="avatar-emoji">{{ avatarEmoji }}</span>
              <el-avatar v-else :size="36" :src="userStore.userInfo?.avatar" />
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">👤 个人中心</el-dropdown-item>
                <el-dropdown-item command="changePassword">🔒 修改密码</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>

  <!-- 移动端 Drawer 菜单 -->
  <el-drawer
    v-model="drawerVisible"
    direction="ltr"
    :with-header="false"
    size="220px"
    class="mobile-drawer"
  >
    <div class="drawer-inner">
      <div class="drawer-logo">
        <h2>🚀 星途补给站</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        class="menu drawer-menu"
        @select="drawerVisible = false"
      >
        <!-- 宇航员菜单 -->
        <template v-if="!userStore.isAdmin()">
          <el-menu-item index="/dashboard" @click="drawerVisible = false"><el-icon><House /></el-icon><span>空间站控制台</span></el-menu-item>
          <el-menu-item index="/mall" @click="drawerVisible = false"><el-icon><Shop /></el-icon><span>能量补给舱</span></el-menu-item>
          <el-menu-item index="/my-points" @click="drawerVisible = false"><el-icon><TrophyBase /></el-icon><span>航行能量轨迹</span></el-menu-item>
          <el-menu-item index="/my-exchanges" @click="drawerVisible = false"><el-icon><ShoppingCart /></el-icon><span>兑换发货舱</span></el-menu-item>
          <el-menu-item index="/tasks" @click="drawerVisible = false"><el-icon><Aim /></el-icon><span>星际任务雷达</span></el-menu-item>
          <el-menu-item index="/wishlist" @click="drawerVisible = false"><el-icon><Star /></el-icon><span>许愿发射台</span></el-menu-item>
          <el-menu-item index="/help" @click="drawerVisible = false"><el-icon><QuestionFilled /></el-icon><span>星际航行指南</span></el-menu-item>
        </template>

        <!-- 舰长/领航员菜单 -->
        <template v-else>
          <el-menu-item index="/admin/dashboard" @click="drawerVisible = false"><el-icon><DataAnalysis /></el-icon><span>舰队指挥中心</span></el-menu-item>
          <el-menu-item index="/admin/thumbs" @click="drawerVisible = false"><el-icon><Lightning /></el-icon><span>能量源控制</span></el-menu-item>
          <el-menu-item index="/admin/task-approval" @click="drawerVisible = false"><el-icon><Checked /></el-icon><span>任务核验舱</span></el-menu-item>
          <el-menu-item index="/admin/exchange-delivery" @click="drawerVisible = false"><el-icon><Box /></el-icon><span>补给调度室</span></el-menu-item>
          <el-menu-item index="/admin/wishlist-approval" @click="drawerVisible = false"><el-icon><Compass /></el-icon><span>蓝图解析室</span></el-menu-item>
          <el-menu-item index="/admin/tasks" @click="drawerVisible = false"><el-icon><Aim /></el-icon><span>任务定义管理</span></el-menu-item>
          <el-menu-item index="/admin/broadcast-settings" @click="drawerVisible = false"><el-icon><Mic /></el-icon><span>星际广播台</span></el-menu-item>
          <template v-if="userStore.isSuperAdmin()">
            <el-menu-item index="/admin/users" @click="drawerVisible = false"><el-icon><UserFilled /></el-icon><span>乘员编制管理</span></el-menu-item>
            <el-menu-item index="/admin/products" @click="drawerVisible = false"><el-icon><Shop /></el-icon><span>补给物资库房</span></el-menu-item>
            <el-menu-item index="/admin/exchanges" @click="drawerVisible = false"><el-icon><List /></el-icon><span>全站星际日志</span></el-menu-item>
            <el-menu-item index="/admin/broadcast-settings" @click="drawerVisible = false"><el-icon><Mic /></el-icon><span>星际广播台</span></el-menu-item>
          </template>
        </template>
      </el-menu>
    </div>
  </el-drawer>

  <!-- 个人中心弹窗 -->
  <el-dialog v-model="profileVisible" title="👨‍🚀 个人中心" width="480px" :border-radius="20" class="profile-dialog">
    <div class="profile-body">
      <div class="current-avatar-wrap">
        <div class="current-avatar">
          <span v-if="!avatarIsUrl" class="current-avatar-emoji">{{ avatarEmoji }}</span>
          <el-avatar v-else :size="90" :src="userStore.userInfo?.avatar" />
        </div>
        <div class="profile-name">{{ userStore.userInfo?.real_name }}</div>
        <el-tag :type="userStore.isSuperAdmin() ? 'danger' : userStore.isAdmin() ? 'warning' : 'primary'" size="small" round>
          {{ userStore.isSuperAdmin() ? '👑 舰长' : userStore.isAdmin() ? '🧭 领航员' : '🚀 宇航员' }}
        </el-tag>
      </div>

      <el-descriptions :column="1" size="small" border class="profile-info">
        <el-descriptions-item label="用户名">{{ userStore.userInfo?.username }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ userStore.userInfo?.email || '未设置' }}</el-descriptions-item>
        <el-descriptions-item label="手机">{{ userStore.userInfo?.phone || '未设置' }}</el-descriptions-item>
        <el-descriptions-item v-if="!userStore.isAdmin()" label="总能量">{{ userStore.userInfo?.total_points ?? 0 }} ⚡</el-descriptions-item>
        <el-descriptions-item v-if="!userStore.isAdmin()" label="可用能量">{{ userStore.userInfo?.available_points ?? 0 }} ⚡</el-descriptions-item>
      </el-descriptions>

      <div class="avatar-section">
        <div class="avatar-section-title">更换头像</div>
        <div class="preset-avatars">
          <div
            v-for="p in presetAvatars"
            :key="p.key"
            class="preset-item"
            :class="{ active: userStore.userInfo?.avatar === p.key }"
            @click="selectPreset(p.key)"
          >
            {{ p.emoji }}
          </div>
        </div>
        <div class="upload-area">
          <el-upload
            :show-file-list="false"
            :before-upload="beforeUpload"
            :http-request="uploadAvatar"
            accept="image/jpeg,image/png,image/gif,image/webp"
          >
            <el-button size="small" plain round>
              <el-icon><Upload /></el-icon> 上传本地图片
            </el-button>
          </el-upload>
          <span class="upload-tip">支持 jpg/png/gif/webp，不超过5MB</span>
        </div>
      </div>
    </div>
    <template #footer>
      <el-button @click="profileVisible = false" round>关闭</el-button>
      <el-button type="primary" @click="router.push('/change-password'); profileVisible = false" round>修改密码</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import {
  House, Shop, TrophyBase, ShoppingCart, Star, Fold, QuestionFilled, Upload, Aim,
  DataAnalysis, Checked, Box, Compass, UserFilled, List, Lightning, Mic
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import api from '@/utils/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const drawerVisible = ref(false)
const profileVisible = ref(false)

const activeMenu = computed(() => route.path)

const presetAvatars = [
  { key: 'preset_1', emoji: '🚀' },
  { key: 'preset_2', emoji: '👨‍🚀' },
  { key: 'preset_3', emoji: '🌟' },
  { key: 'preset_4', emoji: '🪐' },
  { key: 'preset_5', emoji: '🛸' },
  { key: 'preset_6', emoji: '⭐' },
]

const presetMap = Object.fromEntries(presetAvatars.map(p => [p.key, p.emoji]))

const avatarIsUrl = computed(() => {
  const a = userStore.userInfo?.avatar
  return a && (a.startsWith('/') || a.startsWith('http'))
})

const avatarEmoji = computed(() => {
  const a = userStore.userInfo?.avatar
  if (!a) return '🚀'
  return presetMap[a] || '🚀'
})

const selectPreset = async (key) => {
  try {
    await userStore.updateAvatar(key)
    ElMessage.success('头像更换成功 🎉')
  } catch {
    ElMessage.error('头像更换失败')
  }
}

const beforeUpload = (file) => {
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片不能超过5MB')
    return false
  }
  return true
}

const uploadAvatar = async ({ file }) => {
  const formData = new FormData()
  formData.append('file', file)
  try {
    const res = await api.post('/upload/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    await userStore.updateAvatar(res.data.url)
    ElMessage.success('头像上传成功 🎉')
  } catch {
    ElMessage.error('头像上传失败')
  }
}

const handleCommand = (command) => {
  if (command === 'profile') {
    profileVisible.value = true
  } else if (command === 'changePassword') {
    router.push('/change-password')
  } else if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.logout()
      router.push('/login')
    })
  }
}
</script>

<style scoped>
.main-container { min-height: 100vh; }

.sidebar {
  background: linear-gradient(180deg, #7B68EE 0%, #9B59B6 50%, #8E44AD 100%);
  color: white;
}

.logo, .drawer-logo {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  backdrop-filter: blur(4px);
}

.logo h2, .drawer-logo h2 {
  font-size: 17px;
  margin: 0;
  font-weight: 800;
  letter-spacing: 1px;
}

.menu {
  border-right: none;
  background: transparent;
}

.menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.85);
  border-radius: 12px;
  margin: 4px 8px;
  height: 46px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.menu :deep(.el-menu-item:hover) {
  color: white;
  background: rgba(255, 255, 255, 0.25) !important;
}

.menu :deep(.el-menu-item.is-active) {
  color: #7B68EE;
  background: white !important;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.header {
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  box-shadow: 0 4px 20px rgba(255, 107, 157, 0.1);
}

.hamburger-btn {
  display: none;
  color: #7B68EE !important;
  padding: 8px !important;
  min-height: 44px !important;
  min-width: 44px !important;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
}

.role-tag { flex-shrink: 0; }

.username {
  font-size: 15px;
  color: #666;
  font-weight: 600;
}

.avatar-wrap {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B9D, #7B68EE);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 20px;
  box-shadow: 0 2px 10px rgba(123, 104, 238, 0.35);
  transition: transform 0.2s ease;
  overflow: hidden;
}
.avatar-wrap:hover { transform: scale(1.1); }
.avatar-emoji { line-height: 1; }

.main-content {
  padding: 24px;
  background: #FFF8F0;
}

.drawer-inner {
  height: 100%;
  background: linear-gradient(180deg, #7B68EE 0%, #9B59B6 50%, #8E44AD 100%);
  display: flex;
  flex-direction: column;
}
.drawer-menu { flex: 1; overflow-y: auto; }

/* 个人中心弹窗 */
.profile-body { padding: 0 4px; }

.current-avatar-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px 0 16px;
}

.current-avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B9D22, #7B68EE22);
  border: 3px solid #7B68EE44;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 52px;
  overflow: hidden;
}
.current-avatar-emoji { line-height: 1; }

.profile-name {
  font-size: 20px;
  font-weight: 900;
  color: #333;
}

.profile-info { margin: 0 0 20px; }

.avatar-section { border-top: 1px solid #f0e8ff; padding-top: 16px; }
.avatar-section-title {
  font-size: 14px;
  font-weight: 700;
  color: #7B68EE;
  margin-bottom: 12px;
}

.preset-avatars {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.preset-item {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #f5f0ff;
  border: 2px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.preset-item:hover {
  border-color: #7B68EE;
  transform: scale(1.1);
}
.preset-item.active {
  border-color: #FF6B9D;
  background: #fff0f5;
  box-shadow: 0 0 0 3px rgba(255,107,157,0.2);
  transform: scale(1.12);
}

.upload-area {
  display: flex;
  align-items: center;
  gap: 12px;
}
.upload-tip { font-size: 12px; color: #bbb; }

@media (max-width: 768px) {
  .desktop-sidebar { display: none !important; }
  .hamburger-btn {
    display: flex !important;
    align-items: center;
    justify-content: center;
  }
  .main-content { padding: 12px; }
  .menu :deep(.el-menu-item) { height: 52px; }
}
</style>
