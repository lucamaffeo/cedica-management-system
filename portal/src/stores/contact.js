import { defineStore } from 'pinia';
import axios from 'axios';

export const useContactStore = defineStore('contact', {
  state: () => ({
    loading: false,
    error: null,
  }),
  actions: {
    async sendMessage(message) {
      this.loading = true;
      this.error = null; // Reinicia cualquier error previo

      try {
        // Realiza la solicitud al backend
        const response = await axios.post('http://localhost:5000/api/messages/', message);

        if (response.status === 201) {
          // La solicitud fue exitosa, limpia cualquier error
          this.error = null;
        }
      } catch (err) {
        // Manejo de errores detallado
        if (err.response?.data?.errors) {
          this.error = err.response.data.errors;
        } else {
          this.error = 'Error desconocido al enviar el mensaje.';
        }
      } finally {
        // Finaliza el estado de carga
        this.loading = false;
      }
    },
  },
});
