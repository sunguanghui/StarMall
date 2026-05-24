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
      // ===== 宇航员路由 =====
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '空间站控制台' }
      },
      {
        path: '/mall',
        name: 'Mall',
        component: () => import('@/views/Mall.vue'),
        meta: { title: '能量补给舱' }
      },
      {
        path: '/my-points',
        name: 'MyPoints',
        component: () => import('@/views/MyPoints.vue'),
        meta: { title: '航行能量轨迹' }
      },
      {
        path: '/my-exchanges',
        name: 'MyExchanges',
        component: () => import('@/views/MyExchanges.vue'),
        meta: { title: '兑换发货舱' }
      },
      {
        path: '/tasks',
        name: 'Tasks',
        component: () => import('@/views/Tasks.vue'),
        meta: { title: '星际任务雷达' }
      },
      {
        path: '/wishlist',
        name: 'Wishlist',
        component: () => import('@/views/Wishlist.vue'),
        meta: { title: '许愿发射台' }
      },
      {
        path: '/help',
        name: 'Help',
        component: () => import('@/views/Help.vue'),
        meta: { title: '星际航行指南' }
      },
      {
        path: '/change-password',
        name: 'ChangePassword',
        component: () => import('@/views/ChangePassword.vue'),
        meta: { title: '修改密码' }
      },
      // ===== 舰长/领航员路由 =====
      {
        path: '/admin/dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/AdminDashboard.vue'),
        meta: { title: '舰队指挥中心', requireAdmin: true }
      },
      {
        path: '/admin/thumbs',
        name: 'AdminThumbs',
        component: () => import('@/views/admin/Thumbs.vue'),
        meta: { title: '能量源控制', requireAdmin: true }
      },
      {
        path: '/admin/task-approval',
        name: 'TaskApproval',
        component: () => import('@/views/admin/TaskApproval.vue'),
        meta: { title: '任务核验舱', requireAdmin: true }
      },
      {
        path: '/admin/exchange-delivery',
        name: 'ExchangeDelivery',
        component: () => import('@/views/admin/ExchangeDelivery.vue'),
        meta: { title: '补给调度室', requireAdmin: true }
      },
      {
        path: '/admin/wishlist-approval',
        name: 'WishlistApproval',
        component: () => import('@/views/admin/WishlistApproval.vue'),
        meta: { title: '蓝图解析室', requireAdmin: true }
      },
      {
        path: '/admin/users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/Users.vue'),
        meta: { title: '乘员编制管理', requireAdmin: true, requireSuperAdmin: true }
      },
      {
        path: '/admin/products',
        name: 'AdminProducts',
        component: () => import('@/views/admin/Products.vue'),
        meta: { title: '补给物资库房', requireAdmin: true, requireSuperAdmin: true }
      },
      {
        path: '/admin/exchanges',
        name: 'AdminExchanges',
        component: () => import('@/views/admin/Exchanges.vue'),
        meta: { title: '全站星际日志', requireAdmin: true, requireSuperAdmin: true }
      },
      {
        path: '/admin/tasks',
        name: 'AdminTasks',
        component: () => import('@/views/admin/AdminTasks.vue'),
        meta: { title: '任务定义管理', requireAdmin: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  document.title = to.meta.title ? `${to.meta.title} - 星途补给站` : '星途补给站'

  if (to.path === '/login' || to.path === '/register') {
    if (userStore.token && to.path === '/login') {
      next('/')
    } else {
      next()
    }
    return
  }

  if (!userStore.token) {
    next('/login')
    return
  }

  if (to.meta.requireAdmin && userStore.userInfo?.role !== 'admin') {
    next('/dashboard')
    return
  }

  if (to.meta.requireSuperAdmin && !userStore.isSuperAdmin()) {
    next('/admin/dashboard')
    return
  }

  // 管理员访问 /dashboard 自动跳转指挥中心
  if (to.path === '/dashboard' && userStore.userInfo?.role === 'admin') {
    next('/admin/dashboard')
    return
  }

  next()
})

export default router
