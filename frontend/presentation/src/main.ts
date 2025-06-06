// src/main.ts

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

import { router } from './router';  // ← named export olarak router

import './style.css';

// 1) Uygulamayı oluştur
const app = createApp(App);

// 2) Pinia’yı ekle
const pinia = createPinia();
app.use(pinia);

// 3) Auth store’u alıp session restore işini başlat:
import { useAuthStore } from './stores/authStore';
const authStore = useAuthStore();

// initializeAuth() tamamlanana kadar bekle, sonra mount et:
authStore.initializeAuth().then(() => {
  // 4) Router’ı ekle ve uygulamayı mount et
  app.use(router);
  app.mount('#app');
});

// 5) Global navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // Eğer route.meta.requiresAuth varsa ve kullanıcı oturum açmamışsa → login sayfasına gönder
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
    return;
  }

  // Eğer login veya register sayfasına gidiyorsa, ama zaten girişliyse → home sayfasına gönder
  if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next({ name: 'home' });
    return;
  }

  // Aksi hâlde devam et
  next();
});
