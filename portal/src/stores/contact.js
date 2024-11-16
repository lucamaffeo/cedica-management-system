
import { defineStore } from 'pinia'
import axios from 'axios'

export const useContactStore = defineStore('contact', {
  state: () => ({
    contacts: [],
    loading: false,
    error:  null,
  }),
  actions: {
    async fetchContacts() {
      try {
        this.loading = true
        this.error = null
        const response = await axios.get('http://localhost:5000/api/messages/')
        this.contacts = response.data
      }catch{
        this.error = 'Error'
      }
      finally {
        this.loading = false
      }
    },
  },
})