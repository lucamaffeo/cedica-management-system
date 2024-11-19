import { defineStore } from 'pinia';
import axios from 'axios';

export const useContactStore = defineStore('contact', {
  state: () => ({
    loading: false,
    error: null,
    success: null, // Nueva propiedad para manejar mensajes de éxito
  }),
  actions: {
    async sendMessage(message) {
      this.loading = true;
      this.error = null;
      this.success = null;

      try {
        const response = await axios.post('/api/messages', message);

        if (response.status === 201) {
          this.success = 'Mensaje enviado correctamente.';
        }
      } catch (err) {
        if (err.response?.data?.errors) {
          this.error = err.response.data.errors;
        } else {
          this.error = 'Error desconocido al enviar el mensaje.';
        }
      } finally {
        this.loading = false;
      }
    },
  },
});
