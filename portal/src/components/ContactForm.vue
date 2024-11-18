<script setup>
/* global recaptcha */
import { ref, onMounted } from 'vue';
import { useContactStore } from '@/stores/contact';
import { storeToRefs } from 'pinia';
import { RecaptchaV2 } from "vue3-recaptcha-v2";

const handleWidgetId = (widgetId) => {
  console.log("Widget ID: ", widgetId);
};
const handleErrorCallback = () => {
  console.log("Error callback");
};
const handleExpiredCallback = () => {
  console.log("Expired callback");
};
const handleLoadCallback = (response) => {
  console.log("Load callback", response);
};

// Variables
const title = ref('');
const email = ref('');
const description = ref('');
const contactStore = useContactStore();
const { loading, error } = storeToRefs(contactStore);

// Función para enviar el formulario
const submitForm = async () => {
  if (validateForm()) {
    try {
      // Verificar si `grecaptcha` está disponible
      if (typeof grecaptcha === 'undefined') {
        setError('El script de reCAPTCHA no se cargó correctamente.');
        return;
      }

      // Obtener el token de reCAPTCHA
      const recaptchaToken = grecaptcha.getResponse();

      if (!recaptchaToken) {
        setError('Por favor, verifica que no eres un robot.');
        return;
      }

      const messageData = {
        title: title.value,
        email: email.value,
        description: description.value,
        captcha: recaptchaToken
      };

console.log('Datos del mensaje:', messageData); // Verificar los datos antes de enviarlos

await contactStore.sendMessage(messageData);

      if (!error.value) {
        setSuccess('Formulario enviado correctamente.');
        resetForm();
      }
    } catch (err) {
      console.error('Error al enviar el formulario:', err);
      setError('Ocurrió un error, intenta de nuevo.');
    }
  }
};

// Función para validar el formulario
const validateForm = () => {
  if (!title.value.trim()) {
    setError('El titulo es obligatorio.');
    return false;
  }
  if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    setError('Introduce un correo válido.');
    return false;
  }
  if (!description.value.trim()) {
    setError('La descripcion no puede estar vacío.');
    return false;
  }
  return true;
};

// Función para resetear el formulario
const resetForm = () => {
  title.value = '';
  email.value = '';
  description.value = '';
  grecaptcha.reset();
  setError(null);
  setSuccess(null);
};

// Función para establecer un mensaje de error
const setError = (msg) => {
  contactStore.error = msg;
};

// Función para establecer un mensaje de éxito
const setSuccess = (msg) => {
  contactStore.success = msg;
};

</script>

<template>
  <div class="max-w-md mx-auto bg-gray-100 p-8 rounded-lg shadow-md">
    <form @submit.prevent="submitForm" class="space-y-6">
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700">Titulo</label>
        <input type="text" id="title" v-model="title" required class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" />
      </div>
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">Dirección de correo electrónico</label>
        <input type="email" id="email" v-model="email" required class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" />
      </div>
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700">Cuerpo del mensaje</label>
        <textarea id="description" v-model="description" required class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"></textarea>
      </div>
      <RecaptchaV2
        @widget-id="handleWidgetId"
        @error-callback="handleErrorCallback"
        @expired-callback="handleExpiredCallback"
        @load-callback="handleLoadCallback"
      />
      <button type="submit" :disabled="loading" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
        {{ loading ? 'Enviando...' : 'Enviar' }}
      </button>
      <p v-if="loading" class="text-sm text-gray-500">Enviando...</p>
      <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
      <p v-if="contactStore.success" class="text-sm text-green-600">{{ contactStore.success }}</p>
    </form>
  </div>
</template>
