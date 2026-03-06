// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import MainHome from '../components/MainHome.vue'
import News from '../components/News.vue'
import Detection from '../components/Detection.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router