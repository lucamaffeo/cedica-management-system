<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main> 
    <TheWelcome msg="Bienvenidos!" />
  </main>
</template>

<style scoped>
main {
  padding: 2rem;
  background-color: #f9f9f9;
}

section {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
  margin-bottom: 1rem;
}
</style>
