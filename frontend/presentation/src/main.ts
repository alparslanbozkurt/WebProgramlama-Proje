// src/main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import routes from './router'
import './style.css'

// 1) Uygulamayı oluştur
const app = createApp(App)

// 2) Pinia’yı ekle
const pinia = createPinia()
app.use(pinia)

// 3) Router’ı oluştur
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 4) Sayfa halen yüklenmeden önce session’ı /me/ endpoint’iyle restore et
import { useAuthStore } from './stores/authStore'
const authStore = useAuthStore()

// `initializeAuth()` Promise döner; tamamlandıktan sonra mount işlemi yapıyoruz.
authStore.initializeAuth().then(() => {
  // 5) Router’ı ekle ve app’i mount et
  app.use(router)
  app.mount('#app')
})

// 6) Global navigation guard (sayfa geçişlerinde çalışır)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 6A) Eğer route.meta.requiresAuth varsa ve kullanıcı oturum açmamışsa => login sayfasına yönlendir
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // 6B) Eğer route.login veya route.register sayfasını görüntülemek istiyorsa,
  //     ama kullanıcı zaten giriş yapmışsa => ana sayfaya (örneğin 'home') yönlendir.
  if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }

  // Aksi takdirde devam et
  next()
})
