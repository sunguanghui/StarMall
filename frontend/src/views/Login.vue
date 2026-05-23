<template>
  <div class="login-container">

    <!-- 动态星空层 -->
    <div class="stars-layer stars-slow"></div>
    <div class="stars-layer stars-fast"></div>

    <!-- 流星 -->
    <div class="meteor meteor-1"></div>
    <div class="meteor meteor-2"></div>
    <div class="meteor meteor-3"></div>

    <!-- 漂浮星际元素 -->
    <div class="float-el float-star">🌟</div>
    <div class="float-el float-rocket">🚀</div>
    <div class="float-el float-planet">🪐</div>

    <!-- 玻璃态登录卡片 -->
    <div class="login-box">
      <div class="login-header">
        <h1>🚀 星途补给站</h1>
        <p>欢迎登录，飞行员</p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" class="login-form">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="输入飞行员代号"
            size="large"
            :prefix-icon="User"
            class="space-input"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="输入星际密钥"
            size="large"
            :prefix-icon="Lock"
            @keyup.enter="handleLogin"
            class="space-input"
          />
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          :loading="loading"
          @click="handleLogin"
          class="login-button"
        >
          🚀 启动飞船 · 登录
        </el-button>
      </el-form>

      <div class="login-tips">
        <p>🛸 默认账号</p>
        <p>管理员: admin / admin123</p>
        <p>普通用户: zhangsan / user123</p>
      </div>

      <div class="register-link">
        还没有飞行员证？<router-link to="/register">立即注册 ✨</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await userStore.login(form.username, form.password)
      ElMessage.success('登录成功')
      router.push('/')
    } catch (error) {
      console.error('登录失败:', error)
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
/* ===== 全屏容器：深邃星云背景 ===== */
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(120, 40, 200, 0.35) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(255, 107, 157, 0.25) 0%, transparent 55%),
    radial-gradient(ellipse at 60% 80%, rgba(67, 97, 238, 0.3) 0%, transparent 60%),
    linear-gradient(160deg, #0a0015 0%, #1a0533 30%, #0d1b4b 60%, #0a001e 100%);
}

/* ===== 动态星空层 ===== */
.stars-layer {
  position: absolute;
  inset: -100% 0 0 0;
  height: 200%;
  width: 100%;
  pointer-events: none;
}

.stars-slow {
  background-image:
    radial-gradient(1px 1px at 8%  12%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 20% 35%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 35% 8%,  #fff 0%, transparent 100%),
    radial-gradient(2px 2px   at 50% 25%, #ffd 0%, transparent 100%),
    radial-gradient(1px 1px at 65% 48%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 78% 15%, #adf 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 38%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 5%  60%, #ffe 0%, transparent 100%),
    radial-gradient(2px 2px   at 15% 75%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 28% 88%, #ffc 0%, transparent 100%),
    radial-gradient(1px 1px at 42% 68%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 55% 82%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 72%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 90%, #adf 0%, transparent 100%),
    radial-gradient(2px 2px   at 95% 55%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 12% 45%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 38% 52%, #ffd 0%, transparent 100%),
    radial-gradient(1px 1px at 60% 30%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 75% 62%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 48% 95%, #fff 0%, transparent 100%);
  background-size: 100% 50%;
  animation: starDrift 90s linear infinite, twinkleSlow 4s ease-in-out infinite alternate;
  opacity: 0.9;
}

.stars-fast {
  background-image:
    radial-gradient(1px 1px at 6%  22%, #fad 0%, transparent 100%),
    radial-gradient(1px 1px at 18% 58%, #fff 0%, transparent 100%),
    radial-gradient(2px 2px   at 32% 40%, #ffd 0%, transparent 100%),
    radial-gradient(1px 1px at 47% 78%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 62% 18%, #adf 0%, transparent 100%),
    radial-gradient(1px 1px at 76% 65%, #fff 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 88% 32%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 10% 85%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 25% 92%, #ffc 0%, transparent 100%),
    radial-gradient(1px 1px at 52% 72%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 68% 95%, #adf 0%, transparent 100%),
    radial-gradient(2px 2px   at 82% 80%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 93% 70%, #ffe 0%, transparent 100%),
    radial-gradient(1px 1px at 3%  44%, #fff 0%, transparent 100%),
    radial-gradient(1px 1px at 97% 52%, #ffd 0%, transparent 100%);
  background-size: 100% 50%;
  animation: starDrift 55s linear infinite, twinkleFast 2.5s ease-in-out infinite alternate;
  opacity: 0.55;
}

@keyframes starDrift {
  from { transform: translateY(0); }
  to   { transform: translateY(50%); }
}

@keyframes twinkleSlow {
  from { opacity: 0.6; }
  to   { opacity: 1; }
}

@keyframes twinkleFast {
  from { opacity: 0.3; }
  to   { opacity: 0.7; }
}

/* ===== 流星 ===== */
.meteor {
  position: absolute;
  width: 2px;
  height: 80px;
  background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.9) 50%, rgba(255,255,255,0) 100%);
  border-radius: 2px;
  transform: rotate(135deg);
  pointer-events: none;
}

.meteor-1 {
  top: 10%;
  left: 70%;
  animation: meteor 10s linear infinite 0s;
}

.meteor-2 {
  top: 5%;
  left: 40%;
  animation: meteor 10s linear infinite 3.5s;
}

.meteor-3 {
  top: 20%;
  left: 85%;
  animation: meteor 10s linear infinite 7s;
}

@keyframes meteor {
  0%   { transform: rotate(135deg) translate(0, 0);        opacity: 1; }
  10%  { opacity: 1; }
  30%  { transform: rotate(135deg) translate(400px, 400px); opacity: 0; }
  100% { transform: rotate(135deg) translate(400px, 400px); opacity: 0; }
}

/* ===== 漂浮星际元素 ===== */
.float-el {
  position: absolute;
  font-size: 42px;
  pointer-events: none;
  filter: drop-shadow(0 0 12px rgba(255,255,255,0.6));
  z-index: 1;
}

.float-star {
  top: 14%;
  left: 10%;
  animation: floatEl 4s ease-in-out infinite 0s;
}

.float-rocket {
  bottom: 16%;
  right: 9%;
  font-size: 52px;
  animation: floatEl 5s ease-in-out infinite 1.5s;
}

.float-planet {
  top: 60%;
  left: 5%;
  font-size: 36px;
  animation: floatEl 6s ease-in-out infinite 3s;
}

@keyframes floatEl {
  0%, 100% { transform: translateY(0)    rotate(-5deg); }
  50%       { transform: translateY(-22px) rotate(6deg); }
}

/* ===== 玻璃态登录卡片 ===== */
.login-box {
  position: relative;
  z-index: 10;
  width: 420px;
  padding: 44px 40px 36px;
  background: rgba(255, 255, 255, 0.09);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 32px;
  border: 1px solid rgba(255, 255, 255, 0.22);
  box-shadow:
    0 8px 48px rgba(102, 56, 220, 0.45),
    0 0 80px rgba(255, 107, 157, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

/* ===== 登录标题 ===== */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h1 {
  font-size: 28px;
  font-weight: 900;
  color: white;
  text-shadow: 0 0 20px rgba(255, 107, 157, 0.8), 0 2px 8px rgba(0,0,0,0.4);
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.login-header p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.65);
  letter-spacing: 2px;
}

/* ===== 输入框玻璃化 ===== */
.login-form {
  margin-top: 8px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.login-form :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  border-radius: 16px !important;
  box-shadow: none !important;
  backdrop-filter: blur(8px);
  padding: 4px 16px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.login-form :deep(.el-input__wrapper:hover),
.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(255, 107, 157, 0.7) !important;
  box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.2) !important;
}

.login-form :deep(.el-input__inner) {
  color: white !important;
  font-size: 15px;
  height: 40px;
}

.login-form :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.45);
}

.login-form :deep(.el-input__prefix-inner .el-icon) {
  color: rgba(255, 107, 157, 0.9);
  font-size: 18px;
}

.login-form :deep(.el-input__password) {
  color: rgba(255, 255, 255, 0.7) !important;
}

.login-form :deep(.el-form-item__error) {
  color: #ffb3c8;
  padding-left: 8px;
}

/* ===== 登录按钮 ===== */
.login-button {
  width: 100%;
  height: 52px !important;
  margin-top: 8px;
  font-size: 17px !important;
  font-weight: 800 !important;
  letter-spacing: 2px;
  border: none !important;
  border-radius: 26px !important;
  background: linear-gradient(135deg, #FF6B9D 0%, #c850c0 50%, #4158D0 100%) !important;
  background-size: 200% 200% !important;
  box-shadow: 0 6px 28px rgba(255, 107, 157, 0.5), 0 0 0 0 rgba(255, 107, 157, 0) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease, filter 0.25s ease !important;
  animation: btnShimmer 4s ease infinite;
}

@keyframes btnShimmer {
  0%   { background-position: 0%   50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0%   50%; }
}

.login-button:hover {
  transform: scale(1.03) translateY(-2px) !important;
  box-shadow: 0 12px 36px rgba(255, 107, 157, 0.65), 0 0 20px rgba(193, 80, 192, 0.4) !important;
  filter: brightness(1.1);
}

.login-button:active {
  transform: scale(0.97) !important;
  box-shadow: 0 4px 16px rgba(255, 107, 157, 0.4) !important;
}

/* ===== 提示区域 ===== */
.login-tips {
  margin-top: 24px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.55);
  line-height: 2;
}

.login-tips p:first-child {
  font-weight: 700;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2px;
}

/* ===== 注册链接 ===== */
.register-link {
  text-align: center;
  margin-top: 18px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.register-link a {
  color: #FF99BB;
  text-decoration: none;
  margin-left: 4px;
  font-weight: 600;
  transition: color 0.2s ease, text-shadow 0.2s ease;
}

.register-link a:hover {
  color: #FFD6E3;
  text-shadow: 0 0 10px rgba(255, 107, 157, 0.8);
}

/* ===== 移动端适配 ===== */
@media (max-width: 480px) {
  .login-box {
    width: calc(100vw - 32px);
    padding: 36px 24px 28px;
    border-radius: 24px;
  }

  .login-header h1 { font-size: 24px; }
  .float-rocket    { display: none; }
  .float-planet    { display: none; }
  .float-star      { top: 6%; left: 5%; font-size: 32px; }
}
</style>
