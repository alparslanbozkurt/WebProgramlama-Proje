// src/services/api.ts
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

// -----------------------------
// 'api' adında bir Axios instance’ı oluşturuluyor.
// Django REST Framework + Session‐Cookie + CSRF akışı için withCredentials ve xsrf ayarları çok önemli.
// -----------------------------
export const api = axios.create({
  baseURL: '/api',  
  withCredentials: true,        // <<< BURASI ÖNEMLİ (sessionid, csrftoken taşımak için)
  headers: {
    'Content-Type': 'application/json'
  },
  xsrfCookieName: 'csrftoken',   // Django varsayılan CSRF çerez adı
  xsrfHeaderName: 'X-CSRFToken'  // Django DRF tarafında beklenen header
})

// ---------- JWT Desteği (isteğe bağlı) ----------
// Eğer JWT tabanlı “Bearer <token>” kullanacaksanız, 
// burada interceptor’dan yararlanabilirsiniz. Aksi halde silebilirsiniz.
api.interceptors.request.use(
  (config) => {
    try {
      const authStore = useAuthStore()
      if (authStore.accessToken) {
        config.headers = config.headers ?? {}
        config.headers.Authorization = `Bearer ${authStore.accessToken}`
      }
    } catch {
      // Pinia henüz başlatılmamışsa veya store yoksa sessizce devam et
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    // JWT yenileme (refresh token) mekanizması kullanıyorsanız:
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const authStore = useAuthStore()
        const refreshed = await authStore.refreshAccessToken?.()
        if (refreshed && authStore.accessToken) {
          originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`
          return api(originalRequest)
        }
      } catch {
        // Yenileme başarısızsa çıkış yap
      }
      try {
        const authStore = useAuthStore()
        authStore.logout()
      } finally {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// Kullanıcı kodu içinde `useApi()` diyerek bu instance’ı çağırabilirsiniz:
export function useApi() {
  return api
}
