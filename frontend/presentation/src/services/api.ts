import axios, { AxiosInstance } from 'axios'
import { useAuthStore } from '../stores/authStore'

// Create axios instance with base URL
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to attach token to each request
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle token refresh on 401 errors
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()
    
    // If error is 401 and not already trying to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        // Try to refresh the token
        const refreshed = await authStore.refreshAccessToken()
        
        if (refreshed) {
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`
          return apiClient(originalRequest)
        } else {
          // If refresh failed, redirect to login
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

export function useApi() {
  return apiClient
}