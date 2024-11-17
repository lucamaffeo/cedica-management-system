<script setup>
/* global grecaptcha */
import { ref, onMounted } from 'vue';
import { useContactStore } from '@/stores/contact';
import { storeToRefs } from 'pinia';

// Variables
const title = ref('');
const email = ref('');
const description = ref('');
const contactStore = useContactStore();
const { loading, error } = storeToRefs(contactStore);

// ID del contenedor reCAPTCHA
const recaptchaContainerId = 'recaptcha-container';

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

// Función para cargar el script de reCAPTCHA
const loadRecaptchaScript = () => {
  const script = document.createElement('script');
  script.src = 'https://www.google.com/recaptcha/api.js';
  script.async = true;
  script.defer = true;
  script.onload = () => {
    grecaptcha.render(recaptchaContainerId, {
      sitekey: '6Lf0IoEqAAAAAAfIpO43s09xFnVzywmnYpowpP69'
    });
  };
  document.head.appendChild(script);
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

// Cargar el script de reCAPTCHA al montar el componente
onMounted(() => {
  loadRecaptchaScript();
});
</script>

<template>
  <form @submit.prevent="submitForm">
    <div></div>
    <div>
      <label for="title">Titulo</label>
      <input type="text" id="title" v-model="title" required />
    </div>
    <div>
      <label for="email">Dirección de correo electrónico</label>
      <input type="email" id="email" v-model="email" required />
    </div>
    <div>
      <label for="description">Cuerpo del mensaje</label>
      <textarea id="description" v-model="description" required></textarea>
    </div>
    <div id="recaptcha-container"></div>
    <button type="submit" :disabled="loading">{{ loading ? 'Enviando...' : 'Enviar' }}</button>
    <p v-if="loading">Enviando...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="contactStore.success" class="success">{{ contactStore.success }}</p>
  </form>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  color: #000;
  padding: 2rem;
  border: 1px solid #000;
  border-radius: 8px;
}

form div {
  margin-bottom: 1rem;
}

label {
  font-weight: 500;
  font-size: 1.2rem;
  color: #000;
}

input, textarea {
  width: 100%;
  max-width: 400px;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #000;
  border-radius: 4px;
  background-color: #fff;
  color: #000;
}

button {
  padding: 0.7rem 1.5rem;
  font-size: 1rem;
  color: #fff;
  background-color: #000;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #333;
}

p {
  font-size: 1rem;
}

.error {
  color: red;
}

.success {
  color: green;
}
</style>
