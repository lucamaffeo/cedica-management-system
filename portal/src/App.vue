<script setup>
import HelloWorld from './components/HelloWorld.vue';
import NewsView from './views/NewsView.vue';
import ContactView from './views/ContactView.vue';
import AboutView from './views/AboutView.vue';
import TasksView from './views/TasksView.vue';

// Método para hacer scroll a la sección
const scrollToSection = (sectionId) => {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo-cedica.png" width="250" height="125" />
    <HelloWorld msg="Bienvenidos a Cedica!" />
    <!-- Navbar -->
    <nav>
      <a href="#about" @click.prevent="scrollToSection('about')">INFORMACIÓN DE LA INSTITUCIÓN</a>
      <a href="#task" @click.prevent="scrollToSection('task')">TAREAS QUE DESARROLLA</a>
      <a href="#news" @click.prevent="scrollToSection('news')">NOTICIAS</a>
      <a href="#contact" @click.prevent="scrollToSection('contact')">CONTACTO</a>
    </nav>
  </header>

  <main>
    <section id="about">
      <h2>Sobre Nosotros</h2>
      <AboutView />
    </section>

    <section id="task">
      <h2>Tareas</h2>
      <TasksView />
    </section>

    <section id="news">
      <h2>Noticias</h2>
      <NewsView />
    </section>

    <section id="contact">
      <h2>Contacto</h2>
      <ContactView />
    </section>
  </main>
</template>

<style scoped>
/* Header */
header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;
  background-color: #000; /* Fondo negro */
  color: #fff; /* Texto blanco */
}

/* Navbar */
nav {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
}

nav a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}

nav a:hover {
  text-decoration: underline;
}

/* Main content */
main {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 3rem; /* Espacio entre secciones */
}

section {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  padding: 2rem;
  border-bottom: 1px solid #ddd;
}

section h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #00796b;
}

@media (min-width: 1024px) {
  nav {
    gap: 2rem;
  }

  section {
    text-align: left;
  }
}
</style>
