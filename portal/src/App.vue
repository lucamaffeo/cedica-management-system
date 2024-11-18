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
  <header class="flex flex-col items-center py-4 bg-black text-white">
    <img alt="Vue logo" class="logo" src="@/assets/logo-cedica.png" width="250" height="125" />
    <HelloWorld msg="Bienvenidos a Cedica!" />
    <!-- Navbar -->
    <nav class="mt-4 flex justify-center flex-wrap gap-4 lg:gap-8">
      <a href="#about" @click.prevent="scrollToSection('about')" class="text-green-500 font-bold hover:underline">INFORMACIÓN DE LA INSTITUCIÓN</a>
      <a href="#task" @click.prevent="scrollToSection('task')" class="text-green-500 font-bold hover:underline">TAREAS QUE DESARROLLA</a>
      <a href="#news" @click.prevent="scrollToSection('news')" class="text-green-500 font-bold hover:underline">NOTICIAS</a>
      <a href="#contact" @click.prevent="scrollToSection('contact')" class="text-green-500 font-bold hover:underline">CONTACTO</a>
    </nav>
  </header>

  <main class="p-8 flex flex-col gap-12">
    <section id="about" class="w-full max-w-2xl mx-auto text-center lg:text-left p-8 border-b border-gray-300">
      <h2 class="text-2xl mb-4 text-teal-700">Sobre Nosotros</h2>
      <AboutView />
    </section>

    <section id="task" class="w-full max-w-2xl mx-auto text-center lg:text-left p-8 border-b border-gray-300">
      <h2 class="text-2xl mb-4 text-teal-700">Tareas</h2>
      <TasksView />
    </section>

    <section id="news" class="w-full max-w-2xl mx-auto text-center lg:text-left p-8 border-b border-gray-300">
      <h2 class="text-2xl mb-4 text-teal-700">Noticias</h2>
      <NewsView />
    </section>

    <section id="contact" class="w-full max-w-2xl mx-auto text-center lg:text-left p-8 border-b border-gray-300">
      <h2 class="text-2xl mb-4 text-teal-700">Contacto</h2>
      <ContactView />
    </section>
  </main>
</template>
