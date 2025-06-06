import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../services/api'

export interface User {
  id: number
  username: string
  email?: string
  role?: string
  profile_image?: string
  created_at?: string
}

export const useAuthStore = defineStore('auth', () => {
  const api = useApi()

  // --- State ---
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // (JWT destekli isterseniz; yoksa silebilirsiniz)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)

  // --- Computed ---
  const isAuthenticated = computed(() => {
    // Sadece session‐cookie bazlıysa: return user.value !== null
    // JWT bazlı da destekliyoruz diyorsanız:
    return !!user.value || !!accessToken.value
  })

  // --- Helper’lar (JWT için, isterseniz kaldırabilirsiniz) ---
  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)
  }

  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  // --- login() (Session‐Cookie & CSRF akışı) ---
  async function login(username: string, password: string): Promise<boolean> {
    isLoading.value = true
    error.value = null

    try {
      // 1) Önce CSRF cookie’yi al (Django GET /api/accounts/csrf/)
      await api.get('/accounts/csrf/')   // <<< Bu GET isteği sonunda tarayıcıya "csrftoken" çerezi setlenir

      // 2) Ardından POST ile login isteği at 
      //    (tarayıcı, "Set-Cookie: sessionid=..." header’ını kendi içinde saklayacak)
      const res = await api.post('/accounts/login/', {
        username,
        password
      })

      // 3) Eğer 200 dönmüşse, res.data içinde { user_id, username } gelir.
      //    Biz session bazlı girdiğimizi varsayıyoruz:
      user.value = {
        id: res.data.user_id,
        username: res.data.username
      }

      isLoading.value = false
      return true
    } catch (err: any) {
      // Eğer CSRF token eksikse ya da login hatalıysa:
      error.value = err.response?.data?.detail || 'Login failed'
      isLoading.value = false
      return false
    }
  }

  // --- register() (CSRF + kayıt akışı) ---
  async function register(username: string, email: string, password: string): Promise<boolean> {
    isLoading.value = true
    error.value = null

    try {
      // CSRF cookie’yi al
      await api.get('/accounts/csrf/')

      // Ardından register isteği at
      await api.post('/accounts/register/', {
        username,
        email,
        password
      })

      isLoading.value = false
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      isLoading.value = false
      return false
    }
  }

  // --- logout() (Session’ı sunucuda kapat & Pinia’yı temizle) ---
  async function logout() {
    try {
      await api.post('/accounts/logout/')
    } catch {
      // Hata alırsan bile Pinia’daki user’ı null’a çevir:
    } finally {
      user.value = null
      clearTokens()
    }
  }

  // --- initializeAuth() (sayfa ilk yüklendiğinde session’ı yeniden oluştur) ---
  //    Eğer localStorage’da JWT varsa yükle, sonra me/ endpoint’ine bak.
  async function initializeAuth() {
    // 1) JWT varsa yükle
    const storedAccess = localStorage.getItem('accessToken')
    const storedRefresh = localStorage.getItem('refreshToken')
    if (storedAccess && storedRefresh) {
      setTokens(storedAccess, storedRefresh)
      // Burada istersen JWT decode edip user.value’yu ayarlayabilirsin
      // Biz bu örnekte session bazlı meView’i çağıracağız
    }

    // 2) Session bazlı kullanıcı bilgisi almak için MeView’e GET isteği at
    try {
      const res = await api.get('/accounts/me/')
      user.value = {
        id: res.data.user_id,
        username: res.data.username
      }
    } catch {
      // Eğer session geçerli değilse veya 401 dönüyorsa:
      user.value = null
      // Eğer JWT yüklü ise, JWT sonucu user.set edebilirsin
    }
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    accessToken,
    refreshToken,
    login,
    register,
    logout,
    initializeAuth,
    setTokens,
    clearTokens
  }
})
