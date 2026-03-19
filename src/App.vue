<template>
  <div class="app">
    <Header v-if="$route.name !== 'Login'" />
    <div class="router-view-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Header from './Header.vue'

export default {
  name: 'App',
  components: {
    Header
  }
}
</script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
  background-color: #f5f9ff;
  color: #1a2a3a;
  line-height: 1.6;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.router-view-container {
  flex: 1;
  padding: 20px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .router-view-container {
    padding: 10px;
  }
}
</style>