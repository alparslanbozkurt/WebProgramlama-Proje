import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface User {
  id: number
  username: string
  email: string
  profile_image?: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value)

  async function login(username: string, password: string) {
    isLoading.value = true
    error.value = null

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Demo login
      if (username === 'demo' && password === 'demo') {
        user.value = {
          id: 1,
          username: 'demo',
          email: 'demo@example.com'
        }
        localStorage.setItem('user', JSON.stringify(user.value))
        return true
      }
      
      throw new Error('Invalid credentials')
    } catch (e: any) {
      error.value = e.message
      return false
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('user')
  }

  function initializeAuth() {
    const stored = localStorage.getItem('user')
    if (stored) {
      user.value = JSON.parse(stored)
    }
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    login,
    logout,
    initializeAuth
  }
})