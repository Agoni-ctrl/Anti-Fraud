<script setup>
import Header from './components/Header.vue'
</script>

<template>
  <Header></Header>
  <!-- 路由视图，用于显示当前路由对应的组件 -->
  <router-view></router-view>
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