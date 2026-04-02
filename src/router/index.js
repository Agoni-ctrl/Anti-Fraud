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
  // 紧急求助弹窗页面路由
  // {
  //   path: '/emergency',
  //   name: 'Emergency',
  //   component: () => import('../components/EmergencyModal.vue')
  // },
  // 登录/注册页面路由（预留）
  // {
  //   path: '/auth',
  //   name: 'Auth',
  //   component: () => import('../components/Auth.vue')  // 预留，之后创建此组件
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router