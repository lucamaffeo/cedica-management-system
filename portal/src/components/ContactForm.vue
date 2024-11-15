<template>
  <form @submit.prevent="submitForm">
    <div>
      <label for="name">Nombre completo</label>
      <input id="name" v-model="name" required />
    </div>
    <div>
      <label for="email">Correo electrónico</label>
      <input id="email" v-model="email" type="email" required />
    </div>
    <div>
      <label for="message">Mensaje</label>
      <textarea id="message" v-model="message" required></textarea>
    </div>
    <button type="submit">Enviar</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useContactStore } from '@/stores/contact'

const store = useContactStore()

const name = ref('')
const email = ref('')
const message = ref('')

const submitForm = async () => {
  if (validateForm()) {
    try {
      await store.sendMessage({ name: name.value, email: email.value, message: message.value })
      alert('Mensaje enviado con éxito')
      resetForm()
    } catch (error) {
      console.error(error)
      alert('Error al enviar el mensaje')
    }
  }
}

const validateForm = () => {
  return name.value && email.value && message.value && validateEmail(email.value)
}

const validateEmail = (email) => {
  const re = /\S+@\S+\.\S+/
  return re.test(email)
}

const resetForm = () => {
  name.value = ''
  email.value = ''
  message.value = ''
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

form div {
  margin-bottom: 1rem;
}

label {
  font-weight: 500;
  font-size: 1.2rem;
}

input, textarea {
  width: 100%;
  max-width: 400px;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.7rem 1.5rem;
  font-size: 1rem;
  color: #fff;
  background-color: #42b983;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #38a169;
}

@media (min-width: 1024px) {
  form {
    align-items: flex-start;
  }
}
</style>
