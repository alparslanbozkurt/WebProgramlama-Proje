import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

// Import views
import routes from './router'

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Create Pinia store
const pinia = createPinia()

// Create app
const app = createApp(App)

// Add navigation guard to check authentication
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } 
  // Check if route requires specific role
  else if (to.meta.requiredRole && !authStore.hasRole(to.meta.requiredRole)) {
    next({ name: 'home' })
  } 
  // Check if user is already logged in and trying to access login/register
  else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next({ name: 'home' })
  } 
  else {
    next()
  }
})

// Use plugins
app.use(pinia)
app.use(router)

// Mount app
app.mount('#app')

// Import auth store
import { useAuthStore } from './stores/authStore'