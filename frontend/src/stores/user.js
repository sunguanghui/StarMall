import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  const login = async (username, password) => {
    const res = await api.post('/auth/login', { username, password })
    token.value = res.data.token
    userInfo.value = res.data.user
    localStorage.setItem('token', token.value)
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    return res
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  const getUserInfo = async () => {
    const res = await api.get('/auth/info')
    userInfo.value = res.data
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    return res
  }

  const updateAvatar = async (avatar) => {
    const res = await api.post('/auth/avatar', { avatar })
    userInfo.value = { ...userInfo.value, avatar }
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    return res
  }

  const isAdmin = () => {
    return userInfo.value?.role === 'admin'
  }

  const isSuperAdmin = () => {
    return userInfo.value?.role === 'admin' && userInfo.value?.is_super_admin === true
  }

  const setLoginData = (data) => {
    token.value = data.token
    userInfo.value = data.user
    localStorage.setItem('token', token.value)
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
  }

  return {
    token,
    userInfo,
    login,
    logout,
    getUserInfo,
    updateAvatar,
    isAdmin,
    isSuperAdmin,
    setLoginData
  }
})

