<template>
  <div class="login-page">
    <div class="main-container">
      <!-- Logo卡片 -->
      <div class="logo-card">
        <img src="../../assets/images/user/login.png" alt="Anti-Fraud Shield" class="logo-icon">
        <h1 class="logo-title">Anti-Fraud</h1>
        <p class="logo-subtitle">智能反诈 · 守护真实</p>
        <div class="logo-decoration"></div>
      </div>

      <!-- 登录卡片 -->
      <div class="login-card">
        <!-- 关闭按钮 -->
        <button class="close-btn" @click="closeModal">✕</button>

        <div class="login-header">
          <h2 class="login-title">欢迎登录</h2>
          <p class="login-subtitle">请填写您的登录信息</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">
              <font-awesome-icon icon="user" class="input-icon" />
              账号
            </label>
            <input v-model="formData.username" type="text" placeholder="请输入账号" class="form-input" required>
          </div>

          <div class="form-group">
            <label class="form-label">
              <font-awesome-icon icon="lock" class="input-icon" />
              密码
            </label>
            <input v-model="formData.password" type="password" placeholder="请输入密码" class="form-input" required>
          </div>

          <div class="form-group">
            <label class="form-label">
              <font-awesome-icon icon="shield-halved" class="input-icon" />
              验证码
            </label>
            <div class="captcha-wrapper">
              <input v-model="formData.captcha" type="text" placeholder="请输入验证码" class="form-input captcha-input" required>
              <canvas ref="captchaCanvas" @click="generateCaptcha" class="captcha-image" width="100" height="40"></canvas>
            </div>
          </div>

          <div class="form-options">
            <label class="remember-me">
              <input v-model="formData.rememberMe" type="checkbox">
              <span>记住我</span>
            </label>
            <a href="#" class="forgot-link" @click.prevent>忘记密码？</a>
          </div>

          <button type="submit" class="submit-btn">
            立即登录
          </button>
        </form>

        <div class="register-link">
          <span>还没有账号？</span>
          <a href="#" @click.prevent="switchToRegister" class="link">立即注册</a>
        </div>

        <transition name="fade">
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['login-success', 'switch-to-register', 'close-modal'])

const formData = ref({
  username: '',
  password: '',
  captcha: '',
  rememberMe: false
})

const errorMessage = ref('')
const captchaCanvas = ref(null)
let captchaCode = ''

// 生成验证码
const generateCaptcha = () => {
  const canvas = captchaCanvas.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#f0f8ff'
  ctx.fillRect(0, 0, 100, 40)
  
  // 生成随机字符
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let code = ''
  for (let i = 0; i < 4; i++) {
    code += chars[Math.floor(Math.random() * chars.length)]
  }
  captchaCode = code
  
  // 绘制文字
  ctx.font = 'bold 24px Arial'
  ctx.fillStyle = '#0071E3'
  ctx.textBaseline = 'middle'
  for (let i = 0; i < code.length; i++) {
    ctx.save()
    ctx.translate(15 + i * 22, 20)
    ctx.rotate((Math.random() - 0.5) * 0.4)
    ctx.fillText(code[i], 0, 0)
    ctx.restore()
  }
  
  // 绘制干扰线
  ctx.strokeStyle = '#90cdf4'
  ctx.lineWidth = 1
  for (let i = 0; i < 3; i++) {
    ctx.beginPath()
    ctx.moveTo(Math.random() * 100, Math.random() * 40)
    ctx.lineTo(Math.random() * 100, Math.random() * 40)
    ctx.stroke()
  }
}

// 登录处理
const handleLogin = () => {
  // 验证码校验
  if (formData.value.captcha.toUpperCase() !== captchaCode) {
    errorMessage.value = '验证码错误，请重新输入'
    generateCaptcha()
    formData.value.captcha = ''
    return
  }
  
  // 账号密码校验
  if (!formData.value.username) {
    errorMessage.value = '请输入账号'
    return
  }
  
  if (!formData.value.password) {
    errorMessage.value = '请输入密码'
    return
  }
  
  // 模拟登录成功，保存用户信息到 localStorage
  localStorage.setItem('isLoggedIn', 'true')
  localStorage.setItem('username', formData.value.username)
  localStorage.setItem('userNickname', formData.value.username)
  
  // 触发登录成功事件
  emit('login-success')
}

// 切换到注册页面
const switchToRegister = () => {
  emit('switch-to-register')
}

// 关闭弹窗
const closeModal = () => {
  emit('close-modal')
}

// 组件挂载时生成验证码
onMounted(() => {
  generateCaptcha()
})
</script>

<style scoped>
/* 登录页面容器 - 全屏居中 */
.login-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(53, 86, 138, 0.2);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 主容器 - 调整比例，让卡片占据更多空间 */
.main-container {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  border-radius: 16px;
  overflow: visible;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
  max-width: 900px;
  width: 100%;
  min-height: 550px;
  background: white;
}

@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
    max-width: 400px;
    height: auto;
  }
}

/* 左侧Logo卡片 - 增大尺寸 */
.logo-card {
  background: linear-gradient(135deg, #0071E3 0%, #0056b3 100%);
  border-radius: 16px 0 0 16px;
  box-shadow: none;
  padding: 70px 50px;
  position: relative;
  overflow: visible;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-width: 320px;
  min-height: 100%;
}

@media (max-width: 768px) {
  .logo-card {
    border-radius: 16px 16px 0 0;
    padding: 45px 30px;
    min-height: 220px;
  }
}

.logo-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.logo-icon {
  width: auto;
  height: 280px;
  max-width: 100%;
  margin-bottom: 16px;
  animation: float 3s ease-in-out infinite;
  z-index: 1;
  object-fit: contain;
  clip-path: circle(45%);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-8px);
  }
}

.logo-title {
  font-size: 42px;
  font-weight: 800;
  color: white;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-bottom: 8px;
  z-index: 1;
}

.logo-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 1.5px;
  z-index: 1;
}

.logo-decoration {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 100px;
  height: 100px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 右侧登录卡片 - 增大尺寸 */
.login-card {
  background: white;
  border-radius: 0 16px 16px 0;
  box-shadow: none;
  flex: 1.3;
  padding: 45px 40px;
  min-width: 380px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: visible;
  min-height: 100%;
}

/* 关闭按钮样式 */
.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  border: none;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  color: #666;
  z-index: 10;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: rotate(90deg);
  color: #333;
}

@media (max-width: 768px) {
  .login-card {
    border-radius: 0 0 16px 16px;
    padding: 30px 25px;
  }
}

.login-header {
  text-align: center;
  margin-bottom: 20px;
}

.login-title {
  font-size: 26px;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 6px;
}

.login-subtitle {
  font-size: 13px;
  color: #718096;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 15px;
  font-weight: 600;
  color: #2d3748;
  display: flex;
  align-items: center;
  gap: 6px;
}

.input-icon {
  font-size: 16px;
  font-style: normal;
}

.form-input {
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  padding: 14px 16px;
  font-size: 14px;
  color: #1a202c;
  background: #f7fafc;
  transition: all 0.2s ease;
}

.form-input:focus {
  border-color: #0071E3;
  background: white;
  box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.1);
  outline: none;
}

.form-input::placeholder {
  color: #a0aec0;
  font-size: 14px;
}

.captcha-wrapper {
  display: flex;
  gap: 10px;
  align-items: center;
}

.captcha-input {
  flex: 1;
}

.captcha-image {
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  width: 110px;
  height: 44px;
  flex-shrink: 0;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  margin-top: 6px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #4a5568;
  cursor: pointer;
}

.remember-me input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #0071E3;
}

.forgot-link {
  color: #0071E3;
  text-decoration: none;
  font-weight: 500;
}

.forgot-link:hover {
  text-decoration: underline;
}

.submit-btn {
  background: linear-gradient(135deg, #0071E3 0%, #0056b3 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 16px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 12px;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.4);
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 13px;
  color: #718096;
}

.register-link .link {
  color: #0071E3;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  cursor: pointer;
}

.register-link .link:hover {
  text-decoration: underline;
}

.error-message {
  margin-top: 14px;
  padding: 12px;
  background: #fed7d7;
  border: 1px solid #fc8181;
  border-radius: 10px;
  color: #c53030;
  font-size: 13px;
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>