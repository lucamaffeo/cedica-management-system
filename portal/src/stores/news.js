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
        this.loading = true
        this.error = null
        const response = await axios.get('http://localhost:5000/api/articles')
        this.news = response.data
      } catch {
        this.error = 'Error al obtener las noticias'
      } finally {
        this.loading = false
      }
    },
  },
})