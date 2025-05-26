import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {jwtDecode} from 'jwt-decode'
import { useApi } from '../services/api'

export interface User {
  id: number
  username: string
  email?: string
  role?: string
  profile_image?: string
  created_at?: string
}

interface TokenPayload {
  user_id: number
  username: string
  email?: string
  role?: string
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

  const isAuthenticated = computed(() => !!user.value)

  // Token yönetimi
  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)

    // Token’dan kullanıcıyı çözümle (JWT varsa)
    try {
      const decoded = jwtDecode<TokenPayload>(access)
      user.value = {
        id: decoded.user_id,
        username: decoded.username,
        email: decoded.email,
        role: decoded.role
      }
    } catch (err) {
      // Eğer token decode edilemiyorsa yine de giriş yapan kullanıcıyı ayarla
      console.warn('JWT decode edilemedi, kullanıcı response’tan ayarlanacak.')
    }
  }

  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  // Giriş
  async function login(username: string, password: string) {
    isLoading.value = true
    error.value = null
    try {
      const res = await api.post('/accounts/login/', { username, password })

      // Token içermiyorsa kullanıcıyı doğrudan response’tan al
      if (!res.data.access) {
        user.value = {
          id: res.data.user_id,
          username: res.data.username
        }
      } else {
        // Token varsa decode et
        setTokens(res.data.access, res.data.refresh)
      }

      isLoading.value = false
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Login failed'
      isLoading.value = false
      return false
    }
  }

  // Kayıt (şimdilik demo)
  async function register(username: string, email: string, password: string) {
    isLoading.value = true
    error.value = null
    try {
      await api.post('/accounts/register/', { username, email, password })
      isLoading.value = false
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Registration failed'
      isLoading.value = false
      return false
    }
  }

  function logout() {
    clearTokens()
  }

  function initializeAuth() {
    const storedAccess = localStorage.getItem('accessToken')
    const storedRefresh = localStorage.getItem('refreshToken')

    if (storedAccess && storedRefresh) {
      accessToken.value = storedAccess
      refreshToken.value = storedRefresh
      try {
        const decoded = jwtDecode<TokenPayload>(storedAccess)
        user.value = {
          id: decoded.user_id,
          username: decoded.username,
          email: decoded.email,
          role: decoded.role
        }
      } catch (e) {
        clearTokens()
      }
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    initializeAuth
  }
})