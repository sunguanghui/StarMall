<template>
  <el-container class="main-container">
    <!-- 桌面侧边栏 -->
    <el-aside width="200px" class="sidebar desktop-sidebar">
      <div class="logo">
        <h2>🚀 星途补给站</h2>
      </div>
      <el-menu :default-active="activeMenu" router class="menu">
        <el-menu-item index="/dashboard"><el-icon><House /></el-icon><span>首页</span></el-menu-item>
        <el-menu-item index="/mall"><el-icon><Shop /></el-icon><span>能量商城</span></el-menu-item>
        <el-menu-item index="/my-points"><el-icon><TrophyBase /></el-icon><span>我的能量</span></el-menu-item>
        <el-menu-item index="/my-exchanges"><el-icon><ShoppingCart /></el-icon><span>兑换记录</span></el-menu-item>
        <el-menu-item index="/wishlist"><el-icon><Star /></el-icon><span>星际心愿单</span></el-menu-item>
        <el-sub-menu index="/admin" v-if="userStore.isAdmin()">
          <template #title><el-icon><Setting /></el-icon><span>管理中心</span></template>
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
        <!-- 移动端汉堡按钮 -->
        <el-button class="hamburger-btn" @click="drawerVisible = true" text>
          <el-icon :size="24"><Fold /></el-icon>
        </el-button>
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
        <el-menu-item index="/dashboard"><el-icon><House /></el-icon><span>首页</span></el-menu-item>
        <el-menu-item index="/mall"><el-icon><Shop /></el-icon><span>能量商城</span></el-menu-item>
        <el-menu-item index="/my-points"><el-icon><TrophyBase /></el-icon><span>我的能量</span></el-menu-item>
        <el-menu-item index="/my-exchanges"><el-icon><ShoppingCart /></el-icon><span>兑换记录</span></el-menu-item>
        <el-menu-item index="/wishlist"><el-icon><Star /></el-icon><span>星际心愿单</span></el-menu-item>
        <el-sub-menu index="/admin" v-if="userStore.isAdmin()">
          <template #title><el-icon><Setting /></el-icon><span>管理中心</span></template>
          <el-menu-item index="/admin/users" @click="drawerVisible = false">用户管理</el-menu-item>
          <el-menu-item index="/admin/thumbs" @click="drawerVisible = false">发放星辰币</el-menu-item>
          <el-menu-item index="/admin/products" @click="drawerVisible = false">商品管理</el-menu-item>
          <el-menu-item index="/admin/exchanges" @click="drawerVisible = false">兑换管理</el-menu-item>
          <el-menu-item index="/admin/wishlists" @click="drawerVisible = false">心愿审核</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </div>
  </el-drawer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { House, Shop, TrophyBase, ShoppingCart, Setting, Star, Fold } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const drawerVisible = ref(false)

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
  background: linear-gradient(180deg, #7B68EE 0%, #9B59B6 50%, #8E44AD 100%);
  color: white;
}

.logo,
.drawer-logo {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  backdrop-filter: blur(4px);
}

.logo h2,
.drawer-logo h2 {
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

.menu :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.85);
  border-radius: 12px;
  margin: 4px 8px;
  height: 46px;
  font-size: 15px;
}

.menu :deep(.el-sub-menu__title:hover) {
  color: white;
  background: rgba(255, 255, 255, 0.25) !important;
}

.menu :deep(.el-menu--inline) {
  background: rgba(0, 0, 0, 0.1) !important;
  border-radius: 12px;
  margin: 4px 8px;
}

.menu :deep(.el-menu--inline .el-menu-item) {
  background: transparent !important;
  color: rgba(255, 255, 255, 0.8);
  margin: 2px 4px;
  border-radius: 10px;
}

.menu :deep(.el-menu--inline .el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.2) !important;
  color: white;
}

.menu :deep(.el-menu--inline .el-menu-item.is-active) {
  background: white !important;
  color: #7B68EE;
  font-weight: bold;
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
  gap: 15px;
  margin-left: auto;
}

.username {
  font-size: 15px;
  color: #666;
  font-weight: 600;
}

.main-content {
  padding: 24px;
  background: #FFF8F0;
}

/* Drawer 内部样式 */
.drawer-inner {
  height: 100%;
  background: linear-gradient(180deg, #7B68EE 0%, #9B59B6 50%, #8E44AD 100%);
  display: flex;
  flex-direction: column;
}

.drawer-menu {
  flex: 1;
  overflow-y: auto;
}

/* 移动端媒体查询 */
@media (max-width: 768px) {
  .desktop-sidebar {
    display: none !important;
  }

  .hamburger-btn {
    display: flex !important;
    align-items: center;
    justify-content: center;
  }

  .main-content {
    padding: 12px;
  }

  .menu :deep(.el-menu-item) {
    height: 52px;
  }

  .menu :deep(.el-sub-menu__title) {
    height: 52px;
  }
}
</style>
