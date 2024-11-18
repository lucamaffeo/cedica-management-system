import { defineStore } from 'pinia'
import axios from 'axios'

export const useNewsStore = defineStore('news', {
  state: () => ({
    news: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchNews() {
      try {
        this.loading = true;
        this.error = null;
        const response = await axios.get('/api/articles', {
          params: { status: 2 }
        });
        this.news = response.data.data; // Asegúrate de acceder a 'data'
      } catch {
        this.error = 'Error al obtener las noticias';
      } finally {
        this.loading = false;
      }
    }

  },
})
