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

    <!-- Q版宇航员 SVG -->
    <div class="astronaut-wrap">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 200" width="160" height="200" class="astronaut-svg">
        <!-- 背包推进器 -->
        <rect x="55" y="105" width="50" height="38" rx="10" fill="#D0D0E8"/>
        <rect x="62" y="112" width="14" height="10" rx="4" fill="#B0B0D0"/>
        <rect x="84" y="112" width="14" height="10" rx="4" fill="#B0B0D0"/>
        <!-- 喷火 -->
        <ellipse cx="69" cy="148" rx="6" ry="9" fill="#FF8E53" opacity="0.85">
          <animate attributeName="ry" values="9;13;9" dur="0.5s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.85;0.5;0.85" dur="0.5s" repeatCount="indefinite"/>
        </ellipse>
        <ellipse cx="91" cy="148" rx="6" ry="9" fill="#FFD200" opacity="0.85">
          <animate attributeName="ry" values="9;13;9" dur="0.6s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.85;0.5;0.85" dur="0.6s" repeatCount="indefinite"/>
        </ellipse>

        <!-- 身体 (宇航服) -->
        <ellipse cx="80" cy="118" rx="36" ry="38" fill="#F0F0FF"/>
        <!-- 宇航服马卡龙粉装饰条 -->
        <rect x="68" y="108" width="24" height="5" rx="2.5" fill="#FF99BB"/>
        <!-- 宇航服薄荷绿装饰条 -->
        <rect x="60" y="118" width="40" height="4" rx="2" fill="#4ECDC4"/>
        <!-- 胸口控制面板 -->
        <rect x="66" y="125" width="28" height="18" rx="6" fill="#C8C8E8"/>
        <circle cx="73" cy="131" r="3" fill="#FF6B9D"/>
        <circle cx="80" cy="131" r="3" fill="#FFD200"/>
        <circle cx="87" cy="131" r="3" fill="#4ECDC4"/>
        <rect x="70" y="137" width="20" height="3" rx="1.5" fill="#A0A0C8"/>

        <!-- 左臂 -->
        <ellipse cx="40" cy="118" rx="10" ry="18" rx="10" fill="#F0F0FF" transform="rotate(-15 40 118)"/>
        <!-- 左手套 -->
        <ellipse cx="33" cy="132" rx="9" ry="8" fill="#D0D0E8"/>

        <!-- 右臂（伸出去抱星星） -->
        <ellipse cx="120" cy="112" rx="10" ry="18" fill="#F0F0FF" transform="rotate(20 120 112)"/>
        <!-- 右手套 -->
        <ellipse cx="128" cy="126" rx="9" ry="8" fill="#D0D0E8"/>

        <!-- 怀里的星星 ★ -->
        <g transform="translate(118, 130) rotate(-15)">
          <polygon points="16,0 20,11 32,11 22,18 26,29 16,22 6,29 10,18 0,11 12,11" fill="#FFD700"/>
          <polygon points="16,0 20,11 32,11 22,18 26,29 16,22 6,29 10,18 0,11 12,11" fill="url(#starGlow)" opacity="0.6"/>
          <!-- 星星高光 -->
          <circle cx="12" cy="8" r="3" fill="white" opacity="0.5"/>
          <defs>
            <radialGradient id="starGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#FFFACD"/>
              <stop offset="100%" stop-color="#FFD700" stop-opacity="0"/>
            </radialGradient>
          </defs>
        </g>
        <!-- 星星发光动效 -->
        <g transform="translate(118, 130) rotate(-15)" opacity="0">
          <polygon points="16,0 20,11 32,11 22,18 26,29 16,22 6,29 10,18 0,11 12,11" fill="#FFD700"/>
          <animate attributeName="opacity" values="0;0.4;0" dur="1.5s" repeatCount="indefinite"/>
        </g>

        <!-- 头盔外框 -->
        <ellipse cx="80" cy="72" rx="38" ry="40" fill="#E8E8F8"/>
        <!-- 头盔玻璃面罩 -->
        <ellipse cx="80" cy="72" rx="30" ry="32" fill="rgba(180,220,255,0.55)"/>
        <!-- 面罩高光 -->
        <ellipse cx="68" cy="60" rx="8" ry="5" fill="white" opacity="0.45" transform="rotate(-20 68 60)"/>
        <ellipse cx="74" cy="54" rx="4" ry="2.5" fill="white" opacity="0.3" transform="rotate(-20 74 54)"/>

        <!-- 脸 -->
        <ellipse cx="80" cy="73" rx="22" ry="24" fill="#FFDAB9"/>
        <!-- 眼睛 -->
        <ellipse cx="71" cy="67" rx="5" ry="6" fill="#4A3728"/>
        <ellipse cx="89" cy="67" rx="5" ry="6" fill="#4A3728"/>
        <!-- 眼睛高光 -->
        <circle cx="73" cy="65" r="2" fill="white"/>
        <circle cx="91" cy="65" r="2" fill="white"/>
        <!-- 微笑嘴巴 -->
        <path d="M 70 80 Q 80 90 90 80" stroke="#C47B5A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <!-- 腮红 -->
        <ellipse cx="65" cy="77" rx="8" ry="5" fill="#FFB3C8" opacity="0.55"/>
        <ellipse cx="95" cy="77" rx="8" ry="5" fill="#FFB3C8" opacity="0.55"/>

        <!-- 头盔边框装饰 -->
        <ellipse cx="80" cy="72" rx="38" ry="40" fill="none" stroke="#D0D0F0" stroke-width="3"/>
        <!-- 头盔顶部天线 -->
        <line x1="80" y1="32" x2="80" y2="18" stroke="#D0D0E8" stroke-width="3" stroke-linecap="round"/>
        <circle cx="80" cy="15" r="5" fill="#FF99BB"/>
        <circle cx="80" cy="15" r="3" fill="#FFD6E3">
          <animate attributeName="r" values="3;5;3" dur="1.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="1;0.4;1" dur="1.2s" repeatCount="indefinite"/>
        </circle>

        <!-- 腿部 -->
        <rect x="58" y="148" width="20" height="28" rx="10" fill="#E8E8F8"/>
        <rect x="82" y="148" width="20" height="28" rx="10" fill="#E8E8F8"/>
        <!-- 靴子 -->
        <ellipse cx="68" cy="177" rx="13" ry="8" fill="#D0D0E8"/>
        <ellipse cx="92" cy="177" rx="13" ry="8" fill="#D0D0E8"/>
      </svg>
    </div>

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

/* ===== 宇航员 ===== */
.astronaut-wrap {
  position: absolute;
  z-index: 15;
  /* 紧贴登录卡片右侧，垂直居中偏上 */
  left: calc(50% + 210px);
  top: 50%;
  transform: translateY(-60%);
  pointer-events: none;
  animation: astronautFloat 4.5s ease-in-out infinite;
  filter:
    drop-shadow(0 0 18px rgba(255, 107, 157, 0.5))
    drop-shadow(0 8px 24px rgba(0, 0, 0, 0.35));
}

.astronaut-svg {
  display: block;
}

@keyframes astronautFloat {
  0%,  100% { transform: translateY(-60%) rotate(-2deg); }
  50%        { transform: translateY(calc(-60% - 15px)) rotate(2deg); }
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
  .astronaut-wrap  { display: none; }
}

@media (max-width: 900px) and (min-width: 481px) {
  .astronaut-wrap {
    left: calc(50% + 180px);
    transform: translateY(-60%) scale(0.75);
  }
}
</style>
