import { defineStore } from 'pinia';
import axios from 'axios';

export const useApiStore = defineStore('api', {
  state: () => ({
    apiClient: axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL, // URL base desde las variables de entorno
      headers: {
        'Content-Type': 'application/json',
      },
    }),
  }),
});