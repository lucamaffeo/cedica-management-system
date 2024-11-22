<template>
  <header class="flex flex-col items-center py-4 bg-black text-white">
    <img alt="Vue logo" class="logo" src="@/assets/logo-cedica.png" width="250" height="125" />
    <HelloWorld msg="Bienvenidos a Cedica!" />
    <!-- Navbar -->
    <nav class="mt-4 flex justify-center flex-wrap gap-4 lg:gap-8">
      <router-link to="/about" class="text-green-500 font-bold hover:underline">INFORMACIÓN DE LA INSTITUCIÓN</router-link>
      <router-link to="/tasks" class="text-green-500 font-bold hover:underline">TAREAS QUE DESARROLLA LA INSTITUCIÓN</router-link>
      <router-link to="/news" class="text-green-500 font-bold hover:underline">NOTICIAS</router-link>
      <router-link to="/contact" class="text-green-500 font-bold hover:underline">CONTACTO</router-link>
    </nav>
  </header>

  <main class="p-8 flex flex-col gap-12">
    <router-view></router-view>
  </main>
</template>

<script setup>
import HelloWorld from './components/HelloWorld.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
</script>
