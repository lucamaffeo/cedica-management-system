import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { install } from 'vue3-recaptcha-v2'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(install, {
  sitekey: '6Lf0EqAAAAAAfIpO43s09xFnVzywmnYpowpP69',
  language: 'es-419',
  theme: 'dark',
  callback: () => {
    console.log('reCAPTCHA cargado correctamente.');
  },
  'expired-callback': () => {
    console.log('reCAPTCHA expirado.');
  },
  'error-callback': (err) => {
    console.error('Error al cargar reCAPTCHA:', err);
  }
});
app.use(router)



app.mount('#app')
