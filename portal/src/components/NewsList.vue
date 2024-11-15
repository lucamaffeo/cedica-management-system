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
          <th>Fecha de Publicación</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in news" :key="item.id">
          <td>{{ index + 1 }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.summary }}</td>
          <td>{{ item.publication_date }}</td>
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
</script>
