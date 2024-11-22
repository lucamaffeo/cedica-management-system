<template>
  <div class="container mx-auto p-4 text-left">
    <h2 class="text-2xl font-bold mb-4">Lista de Noticias</h2>
    <p v-if="loading" class="text-gray-500">Cargando...</p>
    <p v-if="error" class="text-red-500">{{ error }}</p>
    <table v-if="!loading && news.length" class="min-w-full bg-white border border-gray-200">
      <thead>
        <tr>
          <th class="px-4 py-2 border-b">Fecha de Publicación</th>
          <th class="px-4 py-2 border-b">Título</th>
          <th class="px-4 py-2 border-b">Resumen</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in news" :key="item.id" class="hover:bg-gray-100">
          <td class="px-4 py-2 border-b">{{ formatDate(item.publication_date) || 'No disponible'}}</td>
          <td class="px-4 py-2 border-b">
            <router-link
              :to="{ name: 'news-detail', params: { id: item.id }, query: { newsItem: JSON.stringify(item) } }"
              class="text-blue-500 hover:underline"
            >
              {{ item.title }}
            </router-link>
          </td>
          <td class="px-4 py-2 border-b">{{ item.summary }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && !news.length" class="text-gray-500">No hay noticias para mostrar.</p>
    <VueTailwindPagination
      :current="currentPage"
      :per-page="perPage"
      :total="total"
      @page-changed="onPageChanged"
    />
  </div>
</template>

<script setup>
import { useNewsStore } from '../stores/news';
import { storeToRefs } from 'pinia';
import { onMounted, ref, watch } from 'vue';
import '@ocrv/vue-tailwind-pagination/styles';
import VueTailwindPagination from '@ocrv/vue-tailwind-pagination';
import { useRoute } from 'vue-router';

const currentPage = ref(1);
const perPage = ref(5);

const store = useNewsStore();
const { news, loading, error, total } = storeToRefs(store);

const onPageChanged = (page) => {
  currentPage.value = page;
  fetchNews();
};

const fetchNews = async () => {
  await store.fetchNews(currentPage.value, perPage.value);
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
