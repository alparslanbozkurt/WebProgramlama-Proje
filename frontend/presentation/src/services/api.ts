// src/services/api.ts
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

// 1) axios instance’ını api olarak oluştur
export const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

// 2) request interceptor
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers = config.headers ?? {}
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 3) response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refreshed = await authStore.refreshAccessToken()
        if (refreshed) {
          originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`
          return api(originalRequest)
        } else {
          authStore.logout()
          window.location.href = '/login'
          return Promise.reject(error)
        }
      } catch (refreshError) {
        authStore.logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)

// 4) dilersen bu helper ile de çekebilirsin
export function useApi() {
  return api
}
