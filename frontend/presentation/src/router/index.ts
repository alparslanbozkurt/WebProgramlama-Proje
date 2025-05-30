import { RouteRecordRaw } from 'vue-router'
import { requireAuth, requireAdmin, requireEditor } from '../middleware/auth'

// Import views
import Home from '../views/Home.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import NotFound from '../views/NotFound.vue'

// Define routes
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { title: 'Home' }
  },
  {
    path: '/recommendations',
    name: 'recommendations',
    component: () => import('../components/recommendations/MovieSuggestions.vue'),
    meta: { title: 'AI Recommendations' }
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
    meta: { title: 'My Profile', requiresAuth: true },
    beforeEnter: requireAuth
  },
  {
    path: '/watchlist',
    name: 'watchlist',
    component: () => import('../views/user/Watchlist.vue'),
    meta: { title: 'My Watchlist', requiresAuth: true },
    beforeEnter: requireAuth
  },
  {
    path: '/movies',
    name: 'all-movies',
    component: () => import('../views/content/AllMovies.vue'),
    meta: { title: 'All Movies' }
  },
  {
    path: '/series',
    name: 'all-series',
    component: () => import('../views/content/AllSeries.vue'),
    meta: { title: 'All Series' }
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
    meta: { title: 'Admin Dashboard', requiresAuth: true, requiredRole: 'Admin' },
    beforeEnter: requireAdmin
  },
  {
    path: '/admin/content',
    name: 'admin-content',
    component: () => import('../views/admin/ContentManagement.vue'),
    meta: { title: 'Content Management', requiresAuth: true, requiredRole: 'Admin' },
    beforeEnter: requireAdmin
  },
  {
    path: '/admin/suggestions',
    name: 'admin-suggestions',
    component: () => import('../views/admin/SuggestionsManagement.vue'),
    meta: { title: 'Suggestions Management', requiresAuth: true, requiredRole: 'Admin' },
    beforeEnter: requireAdmin
  },
  {
    path: '/admin/reviews',
    name: 'admin-reviews',
    component: () => import('../views/admin/ReviewManagement.vue'),
    meta: { title: 'Review Management', requiresAuth: true, requiredRole: 'Admin' },
    beforeEnter: requireAdmin
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('../views/admin/UserManagement.vue'),
    meta: { title: 'User Management', requiresAuth: true, requiredRole: 'Admin' },
    beforeEnter: requireAdmin
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: { title: 'Page Not Found' }
  }
]

export default routes