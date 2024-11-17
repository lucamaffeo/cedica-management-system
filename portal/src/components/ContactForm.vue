<script setup>
/* global grecaptcha */
import { ref, onMounted } from 'vue';
import { useContactStore } from '@/stores/contact';
import { storeToRefs } from 'pinia';

// Variables
const name = ref('');
const email = ref('');
const message = ref('');
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
        alert('El script de reCAPTCHA no se cargó correctamente.');
        return;
      }

      // Obtener el token de reCAPTCHA
      const recaptchaToken = grecaptcha.getResponse();

      if (!recaptchaToken) {
        alert('Por favor, verifica que no eres un robot.');
        return;
      }

      // Enviar mensaje al servidor
      await contactStore.sendMessage({
        name: name.value,
        email: email.value,
        message: message.value,
        captcha: recaptchaToken
      });

      if (error.value) {
        alert(error.value);
      } else {
        alert('Formulario enviado correctamente.');
        resetForm();
      }
    } catch (err) {
      console.error('Error al enviar el formulario:', err);
      alert('Ocurrió un error, intenta de nuevo.');
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
  if (!name.value.trim()) {
    alert('El nombre es obligatorio.');
    return false;
  }
  if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    alert('Introduce un correo válido.');
    return false;
  }
  if (!message.value.trim()) {
    alert('El mensaje no puede estar vacío.');
    return false;
  }
  return true;
};

// Función para resetear el formulario
const resetForm = () => {
  name.value = '';
  email.value = '';
  message.value = '';
  grecaptcha.reset();
};

// Cargar el script de reCAPTCHA al montar el componente
onMounted(() => {
  loadRecaptchaScript();
});
</script>

<template>
  <form @submit.prevent="submitForm">
    <div>
      <label for="name">Nombre completo</label>
      <input type="text" id="name" v-model="name" required />
    </div>
    <div>
      <label for="email">Dirección de correo electrónico</label>
      <input type="email" id="email" v-model="email" required />
    </div>
    <div>
      <label for="message">Cuerpo del mensaje</label>
      <textarea id="message" v-model="message" required></textarea>
    </div>
    <div id="recaptcha-container"></div>
    <button type="submit" :disabled="loading">{{ loading ? 'Enviando...' : 'Enviar' }}</button>
    <p v-if="loading">Enviando...</p>
    <p v-if="error">{{ error }}</p>
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
  color: #000;
}
</style>
