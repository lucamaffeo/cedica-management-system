<template>
  <div>
    <h2>Lista de Noticias</h2>
    <p v-if="loading">Cargando...</p>
    <p v-if="error">{{ error }}</p>

    <table v-if="!loading && news.length">
      <thead>
        <tr>
          <th>#</th>
          <th>Título</th>
          <th>Resumen</th>
          <th>Contenido</th>
          <th>Fecha de Publicación</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in news" :key="item.id">
          <td>{{ index + 1 }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.summary }}</td>
          <td>{{ item.content }}</td>
          <td>{{ formatDate(item.publication_date) || 'No disponible'}}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && !news.length">No hay noticias para mostrar.</p>
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

<style scoped>
@import '../assets/style.css';
</style>
