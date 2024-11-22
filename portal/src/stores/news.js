import { defineStore } from 'pinia'
import axios from 'axios'

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
        const response = await axios.get('/api/articles', {
          params: {
            status: 2,
            page: page,
            per_page: perPage
          }
        });
        this.news = response.data.data; // News items for current page
        this.total = response.data.total; // Total number of items
      } catch (error) {
        this.error = 'Error al obtener las noticias';
        console.error(error);
      } finally {
        this.loading = false;
      }
    }
  },
})
