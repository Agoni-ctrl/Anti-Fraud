<script setup>
import { ref, provide } from 'vue'
import Header from './components/Header.vue'
import EmergencyModal from './components/EmergencyModal.vue'

// 控制紧急求助弹窗的显示/隐藏
const showEmergencyModal = ref(false)

// 打开紧急求助弹窗的方法
const openEmergencyModal = () => {
  showEmergencyModal.value = true
}

// 关闭紧急求助弹窗的方法
const closeEmergencyModal = () => {
  showEmergencyModal.value = false
}

// 将打开弹窗的方法提供给所有子组件使用
provide('openEmergencyModal', openEmergencyModal)
</script>

<template>
  <Header />
  <!-- 路由视图，用于显示当前路由对应的组件 -->
  <router-view />
  
  <!-- 紧急求助弹窗 - 浮现在所有内容之上 -->
  <EmergencyModal 
    v-if="showEmergencyModal" 
    @close="closeEmergencyModal"
  />
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
  background-color: #f5fcff;
}
</style>