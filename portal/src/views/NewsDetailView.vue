<template>
  <div class="w-full max-w-2xl mx-auto text-center lg:text-left p-8 border-b border-gray-300 text-lg">
    <h2 class="text-2xl mb-4 text-teal-700">Detalle de la Noticia</h2>
    <div v-if="newsItem">
      <h3 class="text-xl mb-2">{{ newsItem.title }}</h3>
      <p>{{ newsItem.content }}</p>
    </div>
    <div v-else>
      <p>Cargando...</p>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { ref, onMounted } from 'vue';
const route = useRoute();
const newsItem = ref(null);

onMounted(() => {
  if (route.query.newsItem) {
    newsItem.value = JSON.parse(route.query.newsItem);
  }
});

</script>

