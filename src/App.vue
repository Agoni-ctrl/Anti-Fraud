<script setup>
import Header from './components/Header.vue'
import MainHome from './components/MainHome.vue'  
import News from './components/News.vue';
</script>

<template>
  <Header></Header>
  <MainHome></MainHome>  
  <!-- <News></News> -->
</template>

<style scoped>
/* 可以添加全局样式，确保页面布局正确 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
  background-color: #f5fcff; /* 与首页背景保持一致 */
}
</style>