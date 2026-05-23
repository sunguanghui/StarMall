<template>
  <router-view />
</template>

<script setup>
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
</style>



