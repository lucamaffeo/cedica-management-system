<template>
  <div class="News">
    <h1>Noticias</h1>
    <NewsList />
  </div>
</template>

<script setup>
import NewsList from '../components/NewsList.vue'
</script>

<style scoped>
main {
  padding: 2rem;
  background-color: #f9f9f9;
}

h1 {
  color: #333;
  margin-bottom: 1rem;
}
</style>