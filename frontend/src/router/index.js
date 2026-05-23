import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '首页' }
      },
      {
        path: '/mall',
        name: 'Mall',
        component: () => import('@/views/Mall.vue'),
        meta: { title: '积分商城' }
      },
      {
        path: '/my-points',
        name: 'MyPoints',
        component: () => import('@/views/MyPoints.vue'),
        meta: { title: '我的积分' }
      },
      {
        path: '/my-exchanges',
        name: 'MyExchanges',
        component: () => import('@/views/MyExchanges.vue'),
        meta: { title: '兑换记录' }
      },
      {
        path: '/change-password',
        name: 'ChangePassword',
        component: () => import('@/views/ChangePassword.vue'),
        meta: { title: '修改密码' }
      },
      {
        path: '/admin/users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/Users.vue'),
        meta: { title: '用户管理', requireAdmin: true, requireSuperAdmin: true }
      },
      {
        path: '/admin/thumbs',
        name: 'AdminThumbs',
        component: () => import('@/views/admin/Thumbs.vue'),
        meta: { title: '发放星辰币', requireAdmin: true }
      },
      {
        path: '/admin/products',
        name: 'AdminProducts',
        component: () => import('@/views/admin/Products.vue'),
        meta: { title: '商品管理', requireAdmin: true, requireSuperAdmin: true }
      },
      {
        path: '/admin/exchanges',
        name: 'AdminExchanges',
        component: () => import('@/views/admin/Exchanges.vue'),
        meta: { title: '兑换管理', requireAdmin: true, requireSuperAdmin: true }
      },
      {
        path: '/wishlist',
        name: 'Wishlist',
        component: () => import('@/views/Wishlist.vue'),
        meta: { title: '星际心愿单' }
      },
      {
        path: '/help',
        name: 'Help',
        component: () => import('@/views/Help.vue'),
        meta: { title: '航行指南' }
      },
      {
        path: '/admin/wishlists',
        name: 'AdminWishlists',
        component: () => import('@/views/admin/Wishlists.vue'),
        meta: { title: '心愿审核', requireAdmin: true, requireSuperAdmin: true }
      },
      {
        path: '/tasks',
        name: 'Tasks',
        component: () => import('@/views/Tasks.vue'),
        meta: { title: '任务大厅' }
      },
      {
        path: '/admin/tasks',
        name: 'AdminTasks',
        component: () => import('@/views/admin/AdminTasks.vue'),
        meta: { title: '任务管理', requireAdmin: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 星途补给站` : '星途补给站'

  // 登录和注册页面直接放行
  if (to.path === '/login' || to.path === '/register') {
    if (userStore.token && to.path === '/login') {
      next('/')
    } else {
      next()
    }
    return
  }

  // 检查是否登录
  if (!userStore.token) {
    next('/login')
    return
  }

  // 检查管理员权限
  if (to.meta.requireAdmin && userStore.userInfo?.role !== 'admin') {
    next('/')
    return
  }

  // 检查超级管理员权限
  if (to.meta.requireSuperAdmin && !userStore.isSuperAdmin()) {
    next('/dashboard')
    return
  }

  next()
})

export default router
