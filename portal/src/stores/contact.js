import { defineStore } from 'pinia';
import { useApiStore } from './apiStore'; // Importa el store global de la API

export const useContactStore = defineStore('contact', {
  state: () => ({
    loading: false,
    error: null,
    success: null, // Propiedad para manejar mensajes de éxito
  }),
  actions: {
    async sendMessage(message) {
      this.loading = true;
      this.error = null;
      this.success = null;

      try {
        // Obtén apiClient del apiStore
        const apiStore = useApiStore();
        const response = await apiStore.apiClient.post('/api/messages', message);

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
