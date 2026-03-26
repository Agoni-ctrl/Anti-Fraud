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
  // 如果你的人群守护子页面也需要路由，可以添加：
  // {
  //   path: '/guard/elder',
  //   name: 'ElderGuard',
    
  //   component: () => import('../components/GuardElder.vue') 
  // },
  // {
  //   path: '/guard/kids',
  //   name: 'KidsGuard',
  //   component: () => import('../components/GuardKids.vue')
  // },
  // {
  //   path: '/guard/work',
  //   name: 'WorkGuard',
  //   component: () => import('../components/GuardWork.vue')
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router