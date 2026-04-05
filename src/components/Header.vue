<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- 左侧：Logo 和 主导航菜单 -->
      <div class="navbar-left">
        <!-- 网站Logo - 使用router-link跳转到首页 -->
        <router-link to="/" class="logo">
          <!-- Logo图标部分 -->
          <div class="logo-icon-wrapper">
            <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="18" cy="18" r="14" stroke="#4aa3ff" stroke-width="1.5" fill="none"/>
              <circle cx="18" cy="18" r="8" stroke="#4aa3ff" stroke-width="1.2" fill="none" opacity="0.7"/>
              <circle cx="18" cy="18" r="2" fill="#4aa3ff"/>
              <path d="M10 12 C14 8, 22 8, 26 12" stroke="#4aa3ff" stroke-width="1.2" fill="none" opacity="0.6"/>
              <path d="M10 24 C14 28, 22 28, 26 24" stroke="#4aa3ff" stroke-width="1.2" fill="none" opacity="0.6"/>
            </svg>
          </div>
          <div class="logo-text-wrapper">
            <span class="logo-text">Anti-Fraud</span>
            <span class="logo-tagline">反诈·守护</span>
          </div>
        </router-link>

        <!-- 主导航菜单 -->
        <ul class="nav-menu">
          <!-- 首页 -->
          <li class="nav-item">
            <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
              <i class="fas fa-home nav-icon"></i>
              <span>首页</span>
            </router-link>
          </li>

          <!-- AI真伪识别 -->
          <li class="nav-item">
            <router-link to="/detection" class="nav-link" :class="{ active: $route.path === '/detection' }">
              <i class="fa-solid fa-magnifying-glass nav-icon"></i>
              <span>AI真伪识别</span>
            </router-link>
          </li>

          <!-- AI反诈助手 - 使用 clipboard-question 图标 -->
          <li class="nav-item">
            <router-link to="/ai" class="nav-link" :class="{ active: $route.path === '/ai' }">
              <i class="fas fa-robot nav-icon"></i>
              <span>AI反诈助手</span>
            </router-link>
          </li>

          <!-- 人群守护 (下拉菜单) -->
          <li class="nav-item dropdown" @mouseenter="openDropdown('people')" @mouseleave="closeDropdown('people')">
            <a href="#" class="nav-link" @click.prevent>
              <i class="fas fa-users nav-icon"></i>
              <span>人群守护</span>
              <i class="fas fa-chevron-down dropdown-arrow" :class="{ rotated: activeDropdown === 'people' }"></i>
            </a>
            <div class="dropdown-menu" v-show="activeDropdown === 'people'">
              <router-link to="/guard/elder" class="dropdown-item" @click="closeDropdown('people')">
                <i class="fas fa-user-plus dropdown-item-icon"></i>
                银发守护
              </router-link>
              <router-link to="/guard/kids" class="dropdown-item" @click="closeDropdown('people')">
                <i class="fas fa-child dropdown-item-icon"></i>
                亲子课堂
              </router-link>
              <router-link to="/guard/work" class="dropdown-item" @click="closeDropdown('people')">
                <i class="fas fa-briefcase dropdown-item-icon"></i>
                职场防骗
              </router-link>
            </div>
          </li>

          <!-- 最新动态 -->
          <li class="nav-item">
            <router-link to="/news" class="nav-link" :class="{ active: $route.path === '/news' }">
              <i class="fas fa-newspaper nav-icon"></i>
              <span>最新动态</span>
            </router-link>
          </li>

          <!-- 关于我们 -->
          <li class="nav-item">
            <router-link to="/about_us" class="nav-link" :class="{ active: $route.path === '/about_us' }">
              <i class="fas fa-user nav-icon"></i>
              <span>关于我们</span>
            </router-link>
          </li>
        </ul>
      </div>

      <!-- 右上角：紧急求助 + 登录/注册合并按钮 -->
      <div class="navbar-right">
        <button class="emergency-btn" @click="handleEmergency">
          <i class="fas fa-exclamation-triangle btn-icon"></i>
          <span>紧急求助</span>
          <span class="emergency-pulse"></span>
        </button>

        <div v-if="isLoggedIn" class="user-profile">
          <div class="user-dropdown" @mouseenter="openDropdown('user')" @mouseleave="closeDropdown('user')">
            <button class="auth-btn user-btn">
              <i class="fas fa-user btn-icon"></i>
              <span>{{ userNickname || '用户' }}</span>
              <i class="fas fa-chevron-down dropdown-arrow" :class="{ rotated: activeDropdown === 'user' }"></i>
            </button>
            <div class="dropdown-menu" v-show="activeDropdown === 'user'">
              <router-link to="/identity" class="dropdown-item" @click="closeDropdown('user')">
                <i class="fas fa-user-edit dropdown-item-icon"></i>
                身份管理
              </router-link>
              <a href="#" class="dropdown-item" @click.prevent="logout" @click="closeDropdown('user')">
                <i class="fas fa-sign-out-alt dropdown-item-icon"></i>
                退出登录
              </a>
            </div>
          </div>
        </div>
        <button v-else class="auth-btn login-register" @click="goToAuth">
          <i class="fas fa-user-shield btn-icon"></i>
          <span>登录 / 注册</span>
        </button>
      </div>
    </div>

    <!-- 反诈标语滚动条 - anti-fake 图标已改为 fa-brands fa-hornbill -->
    <div class="anti-fraud-ticker">
      <div class="ticker-content">
        <i class="fa-brands fa-hornbill"></i> 全民反诈，你我同行 · 守护财产安全，从我做起 · 96110 反诈专线
      </div>
    </div>
  </nav>
</template>

<script>
import { inject } from 'vue'

export default {
  name: 'AppNavbar',
  data() {
    return {
      activeDropdown: null,
      userNickname: null,
      isLoggedIn: false
    }
  },
  created() {
    // 检查用户是否已登录
    this.checkUserLogin()
  },
  watch: {
    // 监听路由变化，重新检查用户登录状态
    $route() {
      this.checkUserLogin()
    }
  },
  setup() {
    // 注入父组件提供的打开弹窗方法
    const openEmergencyModal = inject('openEmergencyModal', null)
    return { openEmergencyModal }
  },
  methods: {
    checkUserLogin() {
      this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
      this.userNickname = localStorage.getItem('userNickname')
    },
    openDropdown(menu) {
      this.activeDropdown = menu
    },
    closeDropdown(menu) {
      if (this.activeDropdown === menu) {
        this.activeDropdown = null
      }
    },
    handleEmergency() {
      // 调用打开弹窗的方法
      if (this.openEmergencyModal) {
        this.openEmergencyModal()
      } else {
        // 备用方案：如果注入失败，使用 alert
        alert('紧急求助：请拨打 110 或 96110 反诈专线')
      }
    },
    goToAuth() {
      this.$router.push('/login')
    },
    logout() {
      // 清除本地存储
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('userNickname')
      localStorage.removeItem('userIdentity')
      // 更新状态
      this.isLoggedIn = false
      this.userNickname = null
      // 跳转到首页
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
/* 所有样式保持不变 */
.navbar {
  background: linear-gradient(to right, #ffffff, #f0f9ff);
  box-shadow: 0 4px 20px rgba(0, 100, 178, 0.12);
  border-bottom: 2px solid #0064b2;
  padding: 0 2rem 0 2rem;
  font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
  position: sticky;
  top: 0;
  z-index: 1100;
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 2.5rem;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.25rem 0;
  position: relative;
  text-decoration: none;
}

.logo-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text-wrapper {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.logo-text {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(145deg, #0064b2, #1e88e5);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.3px;
}

.logo-tagline {
  font-size: 0.7rem;
  color: #0064b2;
  letter-spacing: 1px;
  font-weight: 500;
  text-transform: uppercase;
  border-left: 2px solid #ff5252;
  padding-left: 6px;
}

.nav-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 0.25rem;
  height: 100%;
  align-items: center;
}

.nav-item {
  height: 100%;
  display: flex;
  align-items: center;
  position: relative;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1rem;
  height: 70%;
  border-radius: 40px;
  text-decoration: none;
  color: #1a2a3a;
  font-weight: 500;
  font-size: 1rem;
  transition: all 0.2s ease;
  white-space: nowrap;
  position: relative;
  overflow: hidden;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: #0064b2;
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 80%;
}

.nav-link:hover {
  background: rgba(0, 100, 178, 0.08);
  color: #0064b2;
}

.nav-icon {
  font-size: 1.3rem;
  color: #0064b2;
}

.nav-link:hover .nav-icon {
  color: #1e88e5;
}

.dropdown-arrow {
  font-size: 0.8rem;
  margin-left: -0.1rem;
  transition: transform 0.2s ease;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 180px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 100, 178, 0.15);
  padding: 0.5rem 0;
  border: 1px solid rgba(0, 100, 178, 0.1);
  z-index: 1200;
  animation: dropdownFade 0.2s ease;
}

@keyframes dropdownFade {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  color: #1a2a3a;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  white-space: nowrap;
  position: relative;
}

.dropdown-item:hover {
  background: rgba(0, 100, 178, 0.05);
  color: #0064b2;
  padding-left: 2rem;
}

.dropdown-item:hover::before {
  content: '🛡️';
  position: absolute;
  left: 0.5rem;
  font-size: 0.8rem;
  opacity: 0.6;
}

.dropdown-item-icon {
  font-size: 1.1rem;
  color: #0064b2;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.emergency-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.4rem;
  border: none;
  border-radius: 40px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #d32f2f;
  color: white;
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.3);
  border: 1px solid #b71c1c;
  position: relative;
  overflow: hidden;
}

.emergency-btn:hover {
  background: #b71c1c;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(211, 47, 47, 0.4);
}

.emergency-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: 40px;
  background: rgba(255, 255, 255, 0.3);
  animation: pulseRing 1.5s infinite;
  pointer-events: none;
}

@keyframes pulseRing {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.2;
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
}

.auth-btn.login-register, .auth-btn.user-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.4rem;
  border: none;
  border-radius: 40px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  background: linear-gradient(145deg, #0064b2, #0099ff);
  color: white;
  border: none;
  box-shadow: 0 4px 10px rgba(0, 100, 178, 0.3);
  position: relative;
  overflow: hidden;
}

.auth-btn.login-register:hover, .auth-btn.user-btn:hover {
  background: linear-gradient(145deg, #0055a0, #0088ee);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 100, 178, 0.2);
}

.user-profile {
  position: relative;
}

.user-dropdown {
  position: relative;
}

.auth-btn.user-btn {
  padding-right: 1.8rem;
}

.auth-btn.user-btn .dropdown-arrow {
  font-size: 0.8rem;
  margin-left: 0.2rem;
  transition: transform 0.2s ease;
}

.btn-icon {
  font-size: 1.1rem;
}

.anti-fraud-ticker {
  width: 100%;
  background: linear-gradient(to right, #0064b2, #0099ff);
  color: white;
  padding: 4px 0;
  font-size: 0.8rem;
  overflow: hidden;
  position: relative;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.ticker-content {
  white-space: nowrap;
  animation: ticker 20s linear infinite;
}

.ticker-content i {
  margin: 0 10px;
  color: #ffd700;
}

@keyframes ticker {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}

.nav-link.active {
  background: rgba(0, 100, 178, 0.12);
  color: #0064b2;
  font-weight: 600;
}

.nav-link.active::after {
  width: 80%;
  background: #0064b2;
}

.nav-link.active .nav-icon {
  color: #0064b2;
}

.dropdown-item.router-link-active {
  background: rgba(0, 100, 178, 0.08);
  color: #0064b2;
}

@media (max-width: 1200px) {
  .navbar-left {
    gap: 1rem;
  }
  .nav-link span:not(.nav-icon) {
    font-size: 0.9rem;
  }
  .nav-link {
    padding: 0 0.75rem;
  }
  .anti-fraud-ticker {
    display: none;
  }
}

@media (max-width: 900px) {
  .navbar-container {
    flex-wrap: wrap;
    height: auto;
    padding: 0.5rem 0;
  }
  .navbar-left {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
  }
  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
  }
  .navbar-right {
    margin-top: 0.25rem;
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>