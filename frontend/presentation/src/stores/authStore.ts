import { defineStore } from 'pinia'
import axios from 'axios'
import { ref, computed } from 'vue'
import { jwtDecode } from 'jwt-decode'
import { useApi } from '../services/api'

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
  const api = useApi()
  
  // State
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  
  // Demo user credentials - DO NOT use in production!
  const demoUser = {
    id: 1,
    username: 'demo_user',
    email: 'demo@example.com',
    role: 'User',
    created_at: '2025-01-01T00:00:00.000Z'
  }
  
  // Computed
  const isAuthenticated = computed(() => !!accessToken.value)
  
  // Methods
  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    
    // Store tokens in localStorage
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)
    
    // For demo: Set demo user
    user.value = demoUser
  }
  
  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    
    // Remove tokens from localStorage
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }
  
  async function getCurrentUser() {
    // For demo: Return the demo user
    // In a real app, this would make an API call to fetch user data
    return user.value
  }
  
  async function login(username: string, password: string) {
    isLoading.value = true
    error.value = null
    
    // Demo login - DO NOT use in production!
    if (username === 'demo_user' && password === 'demo1234') {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // Create demo tokens
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
    
    // Demo registration - DO NOT use in production!
    if (username && email && password) {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // Create demo tokens
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
      // Demo refresh - DO NOT use in production!
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
    return user.value?.role === role
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