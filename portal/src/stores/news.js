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
    async fetchNews(page = 1, perpage = 10, filters = {}) {
      try {
        this.loading = true;
        this.error = null;

        // obtén el cliente api desde el apistore
        const apistore = useApiStore();

        // crear objeto de parámetros base
        const params = {
          status: 2,
          page: page,
          per_page: perpage,
        };

        if (filters.published_from) {
          params.published_from = filters.published_from;
        }

        if (filters.published_to) {
          params.published_to = filters.published_to;
        }

        if (filters.author) {
          params.author = filters.author;
        }

        const response = await apistore.apiClient.get('/api/articles', {
          params: params
        })

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

