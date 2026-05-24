<template>
  <component :is="isAdmin ? AdminDashboard : UserDashboard" />
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import UserDashboard from './UserDashboard.vue'
import AdminDashboard from './admin/AdminDashboard.vue'

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin())
</script>
