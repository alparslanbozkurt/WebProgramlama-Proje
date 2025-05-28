import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../services/api'
import { jwtDecode } from 'jwt-decode'

export interface User {
  id: number
  username: string
  email: string
  role: string
  profile_image?: string
  created_at?: string
}

interface TokenPayload {
  user_id: number
  username: string
  email: string
  role: string
  exp: number
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  
  // Demo user credentials - DO NOT use in production!
  const demoUser = {
    id: 1,
    username: 'demo_admin',
    email: 'admin@example.com',
    role: 'Admin',
    created_at: '2025-01-01T00:00:00.000Z'
  }
  
  // Computed
  const isAuthenticated = computed(() => !!accessToken.value)
  
  // Methods
  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)
    
    user.value = demoUser
  }
  
  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }
  
  async function getCurrentUser() {
    return user.value
  }
  
  async function login(username: string, password: string) {
    isLoading.value = true
    error.value = null
    
    if (username === 'demo_admin' && password === 'admin1234') {
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const demoAccess = 'demo_access_token'
      const demoRefresh = 'demo_refresh_token'
      
      setTokens(demoAccess, demoRefresh)
      isLoading.value = false
      return true
    }
    
    error.value = 'Invalid credentials'
    isLoading.value = false
    return false
  }
  
  async function register(username: string, email: string, password: string) {
    isLoading.value = true
    error.value = null
    
    if (username && email && password) {
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const demoAccess = 'demo_access_token'
      const demoRefresh = 'demo_refresh_token'
      
      setTokens(demoAccess, demoRefresh)
      isLoading.value = false
      return true
    }
    
    error.value = 'Registration failed'
    isLoading.value = false
    return false
  }
  
  async function refreshAccessToken() {
    if (!refreshToken.value) return false
    
    try {
      const demoAccess = 'new_demo_access_token'
      accessToken.value = demoAccess
      localStorage.setItem('accessToken', demoAccess)
      return true
    } catch (e) {
      clearTokens()
      return false
    }
  }
  
  function logout() {
    clearTokens()
  }
  
  function initializeAuth() {
    const storedAccessToken = localStorage.getItem('accessToken')
    const storedRefreshToken = localStorage.getItem('refreshToken')
    
    if (storedAccessToken && storedRefreshToken) {
      setTokens(storedAccessToken, storedRefreshToken)
    }
  }
  
  function hasRole(role: string): boolean {
    return user.value?.role === role || user.value?.role === 'Admin'
  }
  
  return {
    user,
    accessToken,
    isLoading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    refreshAccessToken,
    initializeAuth,
    hasRole,
    getCurrentUser
  }
})