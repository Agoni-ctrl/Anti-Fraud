// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import MainHome from '../components/MainHome.vue'
import News from '../components/News.vue'
import Detection from '../components/Detection.vue'
import AI from '../components/AI.vue'
import AboutUs from '../components/About_us.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: MainHome
  },
  {
    path: '/news',
    name: 'News',
    component: News
  },
  {
    path: '/detection',
    name: 'Detection',
    component: Detection
  },
  {
    path: '/ai-assistant',
    name: 'AIAssistant',
    component: AI
  },
  {
    path: '/about',
    name: 'AboutUs',
    component: AboutUs
  },
  // 人群守护子页面路由
  {
    path: '/guard/elder',
    name: 'ElderGuard',
    component: () => import('../components/GuardElder.vue')
  },
  {
    path: '/guard/kids',
    name: 'KidsGuard',
    component: () => import('../components/GuardKids.vue')
  },
  {
    path: '/guard/work',
    name: 'WorkGuard',
    component: () => import('../components/GuardWork.vue')
  },
  // 用户认证相关路由
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/user/login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../components/user/register.vue')
  },
  {
    path: '/identity',
    name: 'Identity',
    component: () => import('../components/user/identity.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router