// src/router/index.ts
import { RouteRecordRaw } from 'vue-router'
// (Gerekirse kendi middleware’lerinizi import edin)
import Home from '../views/Home.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import Me from '../views/user/Profile.vue'  // Örnek, `/accounts/me/` sonucunu gösteren bir profil sayfası
import NotFound from '../views/NotFound.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { title: 'Login', fullscreen: true }
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { title: 'Register', fullscreen: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: Me,
    meta: { requiresAuth: true, title: 'My Profile' }
  },
  // … diğer rotalarınız …
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: { title: 'Not Found' }
  }
]

export default routes
