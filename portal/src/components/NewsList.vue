<template>
  <div class="container mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">Lista de Noticias</h2>
    <p v-if="loading" class="text-gray-500">Cargando...</p>
    <p v-if="error" class="text-red-500">{{ error }}</p>

    <table v-if="!loading && news.length" class="min-w-full bg-white border border-gray-200">
      <thead>
        <tr>
          <th class="px-4 py-2 border-b">#</th>
          <th class="px-4 py-2 border-b">Título</th>
          <th class="px-4 py-2 border-b">Resumen</th>
          <th class="px-4 py-2 border-b">Contenido</th>
          <th class="px-4 py-2 border-b">Fecha de Publicación</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in news" :key="item.id" class="hover:bg-gray-100">
          <td class="px-4 py-2 border-b">{{ index + 1 }}</td>
          <td class="px-4 py-2 border-b">{{ item.title }}</td>
          <td class="px-4 py-2 border-b">{{ item.summary }}</td>
          <td class="px-4 py-2 border-b">{{ item.content }}</td>
          <td class="px-4 py-2 border-b">{{ formatDate(item.publication_date) || 'No disponible'}}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && !news.length" class="text-gray-500">No hay noticias para mostrar.</p>
  </div>
</template>

<script setup>
import { useNewsStore } from '../stores/news'
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

const store = useNewsStore();
const { news, loading, error } = storeToRefs(store);

const fetchNews = async () => {
  await store.fetchNews();
};

onMounted(() => {
  fetchNews();
});

const formatDate = (dateString) => {
  if (!dateString) return null;
  const date = new Date(dateString);
  return date.toLocaleString([], { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
};
</script>
