<script setup>
import TheWelcome from '../components/TheWelcome.vue'
import ContactForm from '../components/ContactForm.vue'
import NewsList from '../components/NewsList.vue'
</script>

<template>
  <main>
    <TheWelcome />
    <section>
      <h2>Información de la Institución</h2>
      <!-- Información básica de la Institución -->
    </section>
    <section>
      <h2>Tareas que Desarrolla</h2>
      <!-- Tareas que desarrolla la Institución -->
    </section>
    <section>
      <h2>Contacto</h2>
      <ContactForm />
    </section>
    <section>
      <h2>Noticias</h2>
      <NewsList />
    </section>
  </main>
</template>

<style scoped>
main {
  padding: 2rem;
  background-color: #f9f9f9;
}

section {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
  margin-bottom: 1rem;
}

</style>
