<template>
  <div class="main-container">
    <!-- Logo卡片 -->
    <div class="logo-card">
      <div class="logo-icon">🛡️</div>
      <h1 class="logo-title">DeepReal</h1>
      <p class="logo-subtitle">智能反诈 · 守护真实</p>
      <div class="logo-decoration"></div>
    </div>

    <!-- 注册卡片 -->
    <div class="register-card">
      <button class="close-btn" @click="$emit('close-modal')">&times;</button>
      <div class="register-header">
        <h2 class="register-title">创建账号</h2>
        <p class="register-subtitle">填写信息开始注册</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label class="form-label">
            <i class="input-icon">📱</i>
            手机号/邮箱
          </label>
          <input v-model="formData.account" type="text" placeholder="请输入手机号或邮箱" class="form-input"
            required @input="checkAccountFormat">
          <p v-if="accountFormatError" class="error-text">{{ accountFormatError }}</p>
        </div>

        <div class="form-group">
          <label class="form-label">
            <i class="input-icon">🔢</i>
            验证码
          </label>
          <div class="verify-wrapper">
            <input v-model="formData.verifyCode" type="text" placeholder="请输入验证码" class="form-input verify-input"
              required>
            <button type="button" @click="sendVerifyCode"
              :disabled="isSending || countdown > 0 || !isAccountFormatValid"
              :class="['verify-btn', !isAccountFormatValid || isSending || countdown > 0 ? 'disabled' : '']">
              {{ hasSentCode ? (countdown > 0 ? `${countdown}秒` : '重新获取') : '获取验证码' }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">
            <i class="input-icon">🔒</i>
            设置密码
          </label>
          <input v-model="formData.password" type="password" placeholder="请设置密码（至少6位）" class="form-input"
            required>
        </div>

        <div class="form-group">
          <label class="form-label">
            <i class="input-icon">🔐</i>
            确认密码
          </label>
          <input v-model="formData.confirmPassword" type="password" placeholder="请再次输入密码"
            class="form-input" required>
        </div>

        <div class="form-agreement">
          <label class="agreement-label">
            <input v-model="formData.agreeTerms" type="checkbox" required>
            <span>我已阅读并同意<a href="#" class="agreement-link">《用户协议》</a>和<a href="#" class="agreement-link">《隐私政策》</a></span>
          </label>
        </div>

        <button type="submit" class="submit-btn">
          立即注册
        </button>
      </form>

      <div class="login-link">
        <span>已有账号？</span>
        <a href="#" @click.prevent="switchToLogin" class="link">立即登录</a>
      </div>

      <transition name="fade">
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>
      </transition>

      <transition name="fade">
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const emit = defineEmits(['register-success', 'switch-to-login', 'close-modal'])

const formData = ref({
  accountType: 'phone',
  account: '',
  verifyCode: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const isSending = ref(false)
const countdown = ref(0)
const timer = ref(null)
const successMessage = ref('')
const errorMessage = ref('')
const accountFormatError = ref('')
const hasSentCode = ref(false)

const isAccountFormatValid = computed(() => {
  const phoneReg = /^1[3-9]\d{9}$/
  const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return phoneReg.test(formData.value.account) || emailReg.test(formData.value.account)
})

const checkAccountFormat = () => {
  const phoneReg = /^1[3-9]\d{9}$/
  const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!formData.value.account) {
    accountFormatError.value = ''
    return
  }

  if (!phoneReg.test(formData.value.account) && !emailReg.test(formData.value.account)) {
    accountFormatError.value = '请输入正确的手机号或邮箱格式'
  } else {
    accountFormatError.value = ''
  }
}

const sendVerifyCode = () => {
  if (isSending.value || countdown.value > 0 || !isAccountFormatValid.value) {
    return
  }

  if (!formData.value.account) {
    errorMessage.value = '请输入手机号或邮箱'
    return
  }

  isSending.value = true
  errorMessage.value = ''

  setTimeout(() => {
    isSending.value = false
    hasSentCode.value = true
    startCountdown()
    alert('验证码已发送，请注意查收')
  }, 1000)
}

const startCountdown = () => {
  countdown.value = 60
  timer.value = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer.value)
      timer.value = null
    }
  }, 1000)
}

const handleRegister = () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!formData.value.account) {
    errorMessage.value = '请输入手机号或邮箱'
    return
  }

  if (!formData.value.verifyCode) {
    errorMessage.value = '请输入验证码'
    return
  }

  if (!formData.value.password) {
    errorMessage.value = '请设置密码'
    return
  }

  if (formData.value.password.length < 6) {
    errorMessage.value = '密码长度不能少于6位'
    return
  }

  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  if (!formData.value.agreeTerms) {
    errorMessage.value = '请同意用户协议和隐私政策'
    return
  }

  successMessage.value = '注册成功！正在跳转到登录页面...'

  setTimeout(() => {
    emit('register-success')
    emit('switch-to-login')
  }, 2000)
}

const switchToLogin = () => {
  emit('switch-to-login')
}

onBeforeUnmount(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
</script>

<style scoped>
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
  font-size: 80px;
  margin-bottom: 16px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
  animation: float 3s ease-in-out infinite;
  z-index: 1;
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

/* 右侧注册卡片 - 增大尺寸 */
.register-card {
  background: white;
  border-radius: 0 16px 16px 0;
  box-shadow: none;
  flex: 1.3;
  padding: 40px 35px;
  min-width: 380px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: visible;
  min-height: 100%;
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(0, 0, 0, 0.05);
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  z-index: 10;
  transition: all 0.2s ease;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.close-btn:hover {
  color: #333;
  background: rgba(0, 0, 0, 0.1);
  transform: rotate(90deg);
}

@media (max-width: 768px) {
  .register-card {
    border-radius: 0 0 16px 16px;
    padding: 25px 22px;
  }
}

.register-header {
  text-align: center;
  margin-bottom: 18px;
}

.register-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 6px;
}

.register-subtitle {
  font-size: 12px;
  color: #718096;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
  display: flex;
  align-items: center;
  gap: 5px;
}

.input-icon {
  font-size: 15px;
  font-style: normal;
}

.form-input {
  border: 2px solid #e2e8f0;
  border-radius: 9px;
  padding: 13px 15px;
  font-size: 13px;
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
  font-size: 13px;
}

.error-text {
  font-size: 11px;
  color: #e53e3e;
  margin-top: 2px;
}

.verify-wrapper {
  display: flex;
  gap: 8px;
  align-items: center;
}

.verify-input {
  flex: 1;
}

.verify-btn {
  padding: 11px 13px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 9px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  background: linear-gradient(135deg, #0071E3 0%, #0056b3 100%);
  color: white;
}

.verify-btn:hover:not(.disabled) {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.4);
}

.verify-btn.disabled {
  background: #e2e8f0;
  color: #a0aec0;
  cursor: not-allowed;
}

.form-agreement {
  margin-top: 6px;
}

.agreement-label {
  display: flex;
  align-items: flex-start;
  gap: 7px;
  font-size: 11px;
  color: #4a5568;
  cursor: pointer;
  line-height: 1.5;
}

.agreement-label input[type="checkbox"] {
  width: 15px;
  height: 15px;
  accent-color: #0071E3;
  margin-top: 1px;
  flex-shrink: 0;
}

.agreement-link {
  color: #0071E3;
  text-decoration: none;
  font-weight: 500;
}

.agreement-link:hover {
  text-decoration: underline;
}

.submit-btn {
  background: linear-gradient(135deg, #0071E3 0%, #0056b3 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 15px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.4);
}

.login-link {
  text-align: center;
  margin-top: 18px;
  font-size: 12px;
  color: #718096;
}

.login-link .link {
  color: #0071E3;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
}

.login-link .link:hover {
  text-decoration: underline;
}

.success-message {
  margin-top: 12px;
  padding: 11px;
  background: #c6f6d5;
  border: 1px solid #9ae6b4;
  border-radius: 9px;
  color: #22543d;
  font-size: 12px;
  text-align: center;
}

.error-message {
  margin-top: 12px;
  padding: 11px;
  background: #fed7d7;
  border: 1px solid #fc8181;
  border-radius: 9px;
  color: #c53030;
  font-size: 12px;
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
