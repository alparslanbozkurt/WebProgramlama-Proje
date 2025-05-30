import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../services/api'

interface AdminStats {
  totalUsers: number
  totalContent: number
  activeSessions: number
  newUsersToday: number
  contentViews: number
}

interface ChartData {
  labels: string[]
  data: number[]
}

export const useAdminStore = defineStore('admin', () => {
  const api = useApi()
  
  // State
  const stats = ref<AdminStats>({
    totalUsers: 0,
    totalContent: 0,
    activeSessions: 0,
    newUsersToday: 0,
    contentViews: 0
  })
  
  const userActivity = ref<ChartData>({
    labels: [],
    data: []
  })
  
  const contentMetrics = ref<ChartData>({
    labels: [],
    data: []
  })
  
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Actions
  async function fetchDashboardStats() {
    isLoading.value = true
    try {
      // For demo, using mock data
      stats.value = {
        totalUsers: 1247,
        totalContent: 856,
        activeSessions: 42,
        newUsersToday: 15,
        contentViews: 3567
      }
      
      // Mock chart data
      const dates = Array.from({length: 7}, (_, i) => {
        const d = new Date()
        d.setDate(d.getDate() - (6 - i))
        return d.toLocaleDateString('en-US', { weekday: 'short' })
      })
      
      userActivity.value = {
        labels: dates,
        data: Array.from({length: 7}, () => Math.floor(Math.random() * 100))
      }
      
      contentMetrics.value = {
        labels: dates,
        data: Array.from({length: 7}, () => Math.floor(Math.random() * 1000))
      }
    } catch (e: any) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  async function fetchUsers(page: number = 1, search: string = '') {
    isLoading.value = true
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500))
      return {
        users: Array.from({ length: 10 }, (_, i) => ({
          id: i + 1,
          username: `user${i + 1}`,
          email: `user${i + 1}@example.com`,
          role: i < 2 ? 'Admin' : 'User',
          status: i % 5 === 0 ? 'Inactive' : 'Active',
          lastLogin: new Date().toISOString()
        })),
        total: 50
      }
    } catch (e: any) {
      error.value = e.message
      return { users: [], total: 0 }
    } finally {
      isLoading.value = false
    }
  }

  async function fetchContent(page: number = 1, search: string = '') {
    isLoading.value = true
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500))
      return {
        items: Array.from({ length: 10 }, (_, i) => ({
          id: i + 1,
          title: `Content ${i + 1}`,
          type: i % 2 === 0 ? 'movie' : 'series',
          status: i % 5 === 0 ? 'Draft' : 'Published',
          views: Math.floor(Math.random() * 10000),
          createdAt: new Date().toISOString()
        })),
        total: 50
      }
    } catch (e: any) {
      error.value = e.message
      return { items: [], total: 0 }
    } finally {
      isLoading.value = false
    }
  }

  return {
    stats,
    userActivity,
    contentMetrics,
    isLoading,
    error,
    fetchDashboardStats,
    fetchUsers,
    fetchContent
  }
})