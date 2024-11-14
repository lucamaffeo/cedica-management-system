
import { defineStore } from 'pinia'
import axios from 'axios'

export const useContactStore = defineStore('contact', {
  actions: {
    async sendMessage(payload) {
      try {
        await axios.post('/api/messages', payload)
        alert('Mensaje enviado con éxito')
      } catch (error) {
        console.error(error)
        alert('Error al enviar el mensaje')
      }
    }
  }
})