import { RouteRecordRaw } from 'vue-router'

// Import views
import Home     from '../views/Home.vue'
import NotFound from '../views/NotFound.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'


// Define routes
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { title: 'Home' }
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
    component: () => import('../views/user/Profile.vue'),
    meta: { title: 'My Profile', requiresAuth: true }
  },
  {
    path: '/watchlist',
    name: 'watchlist',
    component: () => import('../views/user/Watchlist.vue'),
    meta: { title: 'My Watchlist', requiresAuth: true }
  },
  {
    path: '/movie/:id',
    name: 'movie-detail',
    component: () => import('../views/content/MovieDetail.vue'),
    meta: { title: 'Movie Details' }
  },
  {
    path: '/series/:id',
    name: 'series-detail',
    component: () => import('../views/content/SeriesDetail.vue'),
    meta: { title: 'Series Details' }
  },
  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('../views/admin/Dashboard.vue'),
    meta: { title: 'Admin Dashboard', requiresAuth: true, requiredRole: 'Admin' }
  },
  {
    path: '/admin/content',
    name: 'admin-content',
    component: () => import('../views/admin/ContentManagement.vue'),
    meta: { title: 'Content Management', requiresAuth: true, requiredRole: 'Admin' }
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('../views/admin/UserManagement.vue'),
    meta: { title: 'User Management', requiresAuth: true, requiredRole: 'Admin' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: { title: 'Page Not Found' }
  }
]

export default routes