<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const news = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/articles')
    news.value = response.data.data
  } catch (error) {
    console.error('Error al obtener las noticias', error)
  }
})
</script>

<template>
  <div>
    <div v-for="item in news" :key="item.id" class="news-item">
      <h3>{{ item.title }}</h3>
      <p>{{ item.summary }}</p>
      <small>{{ item.publication_date }}</small>
      <a :href="`/news/${item.id}`">Leer más</a>
    </div>
  </div>
</template>