
import { defineStore } from 'pinia'
import axios from 'axios'

export const useNewsStore = defineStore('news', {
  state: () => ({
    news: []
  }),
  actions: {
    async fetchNews() {
      try {
        const response = await axios.get('/api/articles')
        this.news = response.data.data
        return this.news
      } catch (error) {
        console.error('Error al obtener las noticias', error)
      }
    }
  }
})