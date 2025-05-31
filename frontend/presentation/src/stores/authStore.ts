import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../services/api'
import { jwtDecode } from 'jwt-decode'

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

  // Computed
  const isAuthenticated = computed(() => !!accessToken.value)

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
      // Eğer token decode edilemiyorsa kullanıcıyı null yapabilirsin
      user.value = null
      console.warn('JWT decode edilemedi, kullanıcı ayarlanamadı.')
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
      if (res.data.access && res.data.refresh) {
        setTokens(res.data.access, res.data.refresh)
      } else {
        // Token gelmediyse user'ı manuel ayarla
        user.value = {
          id: res.data.user_id,
          username: res.data.username
        }
      }
      isLoading.value = false
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Login failed'
      isLoading.value = false
      return false
    }
  }

  // Kayıt
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