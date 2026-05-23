<template>
  <el-container class="main-container">
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <h2>🚀 星途补给站</h2>
      </div>

      <el-menu
        :default-active="activeMenu"
        router
        class="menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>

        <el-menu-item index="/mall">
          <el-icon><Shop /></el-icon>
          <span>能量商城</span>
        </el-menu-item>

        <el-menu-item index="/my-points">
          <el-icon><TrophyBase /></el-icon>
          <span>我的能量</span>
        </el-menu-item>

        <el-menu-item index="/my-exchanges">
          <el-icon><ShoppingCart /></el-icon>
          <span>兑换记录</span>
        </el-menu-item>

        <el-menu-item index="/wishlist">
          <el-icon><Star /></el-icon>
          <span>星际心愿单</span>
        </el-menu-item>

        <el-sub-menu index="/admin" v-if="userStore.isAdmin()">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>管理中心</span>
          </template>
          <el-menu-item index="/admin/users">用户管理</el-menu-item>
          <el-menu-item index="/admin/thumbs">发放星辰币</el-menu-item>
          <el-menu-item index="/admin/products">商品管理</el-menu-item>
          <el-menu-item index="/admin/exchanges">兑换管理</el-menu-item>
          <el-menu-item index="/admin/wishlists">心愿审核</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-right">
          <span class="username">{{ userStore.userInfo?.real_name }}</span>
          <el-dropdown @command="handleCommand">
            <el-avatar :size="32" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="changePassword">修改密码</el-dropdown-item>
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
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { House, Shop, TrophyBase, ShoppingCart, Setting, Star } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleCommand = (command) => {
  if (command === 'changePassword') {
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
.main-container {
  min-height: 100vh;
}

.sidebar {
  background: #001529;
  color: white;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #002140;
  color: white;
}

.logo h2 {
  font-size: 18px;
  margin: 0;
}

.menu {
  border-right: none;
  background: #001529;
}

.menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.65);
}

.menu :deep(.el-menu-item:hover),
.menu :deep(.el-menu-item.is-active) {
  color: white;
  background: #1890ff !important;
}

.menu :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.65);
}

.menu :deep(.el-sub-menu__title:hover) {
  color: white;
  background: rgba(255, 255, 255, 0.1) !important;
}

.menu :deep(.el-menu--inline) {
  background: #000c17 !important;
}

.menu :deep(.el-menu--inline .el-menu-item) {
  background: #000c17 !important;
  color: rgba(255, 255, 255, 0.65);
}

.menu :deep(.el-menu--inline .el-menu-item:hover) {
  background: #1890ff !important;
  color: white;
}

.menu :deep(.el-menu--inline .el-menu-item.is-active) {
  background: #1890ff !important;
  color: white;
}

.header {
  background: white;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  font-size: 14px;
  color: #666;
}

.main-content {
  padding: 20px;
  background: #f0f2f5;
}
</style>
