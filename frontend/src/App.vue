<template>
  <router-view />
  <!-- PWA 安装提示横幅 -->
  <div v-if="showInstallBanner" class="pwa-install-banner">
    <span>📱 添加「星途补给站」到主屏幕，享受更好体验！</span>
    <div class="pwa-banner-btns">
      <button class="pwa-btn-install" @click="installPWA">立即安装</button>
      <button class="pwa-btn-dismiss" @click="dismissBanner">稍后再说</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const showInstallBanner = ref(false)
let deferredPrompt = null

onMounted(() => {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt = e
    showInstallBanner.value = true
  })
})

const installPWA = async () => {
  if (!deferredPrompt) return
  deferredPrompt.prompt()
  const { outcome } = await deferredPrompt.userChoice
  if (outcome === 'accepted') {
    showInstallBanner.value = false
  }
  deferredPrompt = null
}

const dismissBanner = () => {
  showInstallBanner.value = false
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #FFF8F0;
  font-size: 15px;
}

#app {
  min-height: 100vh;
}

:root {
  --el-color-primary: #FF6B9D;
  --el-color-primary-light-3: #FF99BB;
  --el-color-primary-light-5: #FFBBCC;
  --el-color-primary-light-7: #FFD6E3;
  --el-color-primary-light-9: #FFF0F5;
  --el-color-primary-dark-2: #E0507F;
  --el-border-radius-base: 16px;
  --el-border-radius-small: 12px;
  --el-border-radius-round: 24px;
}

.el-card {
  border: none !important;
  border-radius: 20px !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08) !important;
}

.el-button {
  border-radius: 24px !important;
}

.el-input__wrapper {
  border-radius: 16px !important;
}

.el-tag {
  border-radius: 12px !important;
}

.el-dialog {
  border-radius: 24px !important;
  overflow: hidden;
}

/* Mobile touch targets */
@media (max-width: 768px) {
  .el-button {
    min-height: 44px;
  }
  .el-input__wrapper {
    min-height: 44px;
  }
}

/* Mobile drawer panel */
.mobile-drawer .el-drawer__body {
  padding: 0 !important;
  overflow: hidden;
}

/* PWA 安装横幅 */
.pwa-install-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, #7B68EE, #FF6B9D);
  color: white;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  z-index: 9999;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
  font-size: 14px;
  flex-wrap: wrap;
}

.pwa-banner-btns {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.pwa-btn-install {
  background: white;
  color: #7B68EE;
  border: none;
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.pwa-btn-dismiss {
  background: transparent;
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 13px;
  cursor: pointer;
}
</style>



