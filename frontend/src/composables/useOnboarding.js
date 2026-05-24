import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'

const STORAGE_KEY = (userId) => `starway_onboarding_completed_${userId}`

// 宇航员（普通用户）引导步骤
const userSteps = () => [
  {
    element: '#onboard-user-points',
    popover: {
      title: '🌟 欢迎登舰！',
      description: '这是你的专属星辰币小金库。完成任务就能让它越来越满哦！',
      side: 'right',
      align: 'center'
    }
  },
  {
    element: '#onboard-menu-tasks',
    popover: {
      title: '🚀 获取能量',
      description: '每天来这里接取巡航任务，完成后就能赚取星辰币啦。',
      side: 'right',
      align: 'center'
    }
  },
  {
    element: '#onboard-menu-mall',
    popover: {
      title: '🎁 兑换战利品',
      description: '能量攒够了？来补给舱挑选你心仪的奖励吧！',
      side: 'right',
      align: 'center'
    }
  }
]

// 舰长/领航员（管理员）引导步骤
const adminSteps = () => {
  const hasExchangesLog = !!document.getElementById('onboard-menu-exchanges')
  const logStep = hasExchangesLog
    ? {
        element: '#onboard-menu-exchanges',
        popover: {
          title: '📖 航行日志',
          description: '全站的每一笔能量流转、每一次奖励发放，都在这里清清楚楚地记录着。',
          side: 'right',
          align: 'center'
        }
      }
    : {
        element: '#onboard-menu-task-def',
        popover: {
          title: '📖 任务定义管理',
          description: '在这里配置任务类型，决定宇航员们能接到哪些巡航任务。',
          side: 'right',
          align: 'center'
        }
      }

  return [
    {
      element: '#onboard-admin-crew',
      popover: {
        title: '👨‍🚀 舰队指挥官，欢迎上任',
        description: '在这里您可以俯瞰全舰队成员的状态，并随时给他们手动注入能量。',
        side: 'top',
        align: 'center'
      }
    },
    {
      element: '#onboard-menu-task-approval',
      popover: {
        title: '📝 审批中心',
        description: '小宇航员们提交的日常任务和主线探索，都在这里等您查阅和批准。',
        side: 'right',
        align: 'center'
      }
    },
    logStep
  ]
}

// 创建 driver 实例（星途粉紫配色通过 CSS 变量覆盖）
const makeDriver = () =>
  driver({
    animate: true,
    smoothScroll: true,
    allowClose: true,
    overlayOpacity: 0.65,
    stagePadding: 8,
    stageRadius: 16,
    popoverClass: 'starway-popover',
    nextBtnText: '下一站 →',
    prevBtnText: '← 返回',
    doneBtnText: '起航！🚀',
    progressText: '{{current}} / {{total}}'
  })

export function useOnboarding(userStore) {
  const userId = userStore.userInfo?.id

  const isCompleted = () => {
    if (!userId) return true
    return localStorage.getItem(STORAGE_KEY(userId)) === 'true'
  }

  const markCompleted = () => {
    if (userId) localStorage.setItem(STORAGE_KEY(userId), 'true')
  }

  const play = (force = false) => {
    if (!force && isCompleted()) return

    const isAdmin = userStore.isAdmin()
    const steps = isAdmin ? adminSteps() : userSteps()

    // 过滤掉 DOM 中不存在的锚点（防止 v-if 导致元素缺失时崩溃）
    const validSteps = steps.filter(
      (s) => !s.element || !!document.querySelector(s.element)
    )
    if (validSteps.length === 0) return

    const driverObj = makeDriver()
    driverObj.setSteps(validSteps)
    driverObj.drive()

    // 监听完成事件：最后一步 Next 或点叉关闭均视为完成
    const origDestroy = driverObj.destroy.bind(driverObj)
    driverObj.destroy = () => {
      markCompleted()
      origDestroy()
    }
  }

  const autoPlay = () => {
    if (!isCompleted()) play(false)
  }

  return { play, autoPlay, isCompleted, markCompleted }
}
