import { defineStore } from 'pinia';
import { useApiStore } from './apiStore'; // Importa el store de la API

export const useNewsStore = defineStore('news', {
  state: () => ({
    news: [],
    loading: false,
    error: null,
    total: 0,
  }),
  actions: {
    async fetchNews(page = 1, perPage = 10) {
      try {
        this.loading = true;
        this.error = null;

        // Obtén el cliente API desde el apiStore
        const apiStore = useApiStore();
        const response = await apiStore.apiClient.get('/api/articles', {
          params: {
            status: 2,
            page: page,
            per_page: perPage,
          },
        });

        // Actualiza los datos en el estado
        this.news = response.data.data; // Noticias para la página actual
        this.total = response.data.total; // Total de artículos
      } catch (error) {
        this.error = 'Error al obtener las noticias';
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
  },
});

