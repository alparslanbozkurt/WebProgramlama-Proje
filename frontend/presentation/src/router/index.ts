// src/router/index.ts

import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

/*
  Klasör yapına göre views altındaki dosyalar:

  src/
  └─ views/
     ├─ admin/           (…)
     ├─ auth/
     │   ├─ Login.vue
     │   └─ Register.vue
     ├─ content/
     │   ├─ AllMovies.vue
     │   ├─ AllSeries.vue
     │   ├─ MovieDetail.vue
     │   └─ SeriesDetail.vue
     ├─ recommendations/
     │   └─ MovieSuggestions.vue    ← AI öneri sayfası için
     ├─ user/
     │   ├─ Profile.vue
     │   └─ Watchlist.vue
     ├─ Home.vue
     └─ NotFound.vue
*/

// 1) Her bir route’un component’ini doğru klasör yoluyla import edin:
import HomeView             from '../views/Home.vue';

import AllMoviesView        from '../views/content/AllMovies.vue';
import AllSeriesView        from '../views/content/AllSeries.vue';
import MovieDetailView      from '../views/content/MovieDetail.vue';
import SeriesDetailView     from '../views/content/SeriesDetail.vue';

import MovieSuggestionsView from '../components/recommendations/MovieSuggestions.vue';  // AI öneri sayfası

import ProfileView          from '../views/user/Profile.vue';
import WatchlistView        from '../views/user/Watchlist.vue';

import LoginView            from '../views/auth/Login.vue';
import RegisterView         from '../views/auth/Register.vue';

import NotFoundView         from '../views/NotFound.vue';

// 2) Route dizisini (routes array) aşağıdaki gibi oluşturun:
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // AI öneri sayfası:
  {
    path: '/ai-recommendations',
    name: 'aiRecommendations',
    component: MovieSuggestionsView
  },
  // Filmler ve film detayları:
  {
    path: '/movies',
    name: 'allMovies',
    component: AllMoviesView
  },
  {
    path: '/movies/:id',
    name: 'movieDetail',
    component: MovieDetailView,
    props: true
  },
  // Diziler ve dizi detayları:
  {
    path: '/series',
    name: 'allSeries',
    component: AllSeriesView
  },
  {
    path: '/series/:id',
    name: 'seriesDetail',
    component: SeriesDetailView,
    props: true
  },
  // Kullanıcı profili / izleme listesi:
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/watchlist',
    name: 'watchlist',
    component: WatchlistView,
    meta: { requiresAuth: true }
  },
  // Auth (giriş/kayıt):
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  // Diğer tüm eşleşmeyen URL’ler:
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView
  }
];

// 3) Router instance’ını oluşturup export edin:
export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});
