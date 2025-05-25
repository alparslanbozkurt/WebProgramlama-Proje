<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { useAuthStore } from '../../stores/authStore'
import { io } from 'socket.io-client'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const authStore = useAuthStore()
const isLoading = ref(true)

// Statistics
const totalUsers = ref(0)
const totalContent = ref(0)
const activeSessions = ref(0)
const newUsersToday = ref(0)
const contentViews = ref(0)

// Chart data
const userActivityData = ref({
  labels: [],
  datasets: [{
    label: 'User Activity',
    data: [],
    borderColor: '#4F46E5',
    tension: 0.4
  }]
})

const contentMetricsData = ref({
  labels: [],
  datasets: [{
    label: 'Content Views',
    data: [],
    borderColor: '#EC4899',
    tension: 0.4
  }]
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      },
      ticks: {
        color: '#9CA3AF'
      }
    },
    x: {
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      },
      ticks: {
        color: '#9CA3AF'
      }
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#9CA3AF'
      }
    }
  }
}

// Mock data generation
function generateMockData() {
  const now = new Date()
  const labels = Array.from({length: 7}, (_, i) => {
    const d = new Date(now)
    d.setDate(d.getDate() - (6 - i))
    return d.toLocaleDateString('en-US', { weekday: 'short' })
  })
  
  return {
    labels,
    data: Array.from({length: 7}, () => Math.floor(Math.random() * 100))
  }
}

// Initialize real-time updates
function initializeRealTimeUpdates() {
  const socket = io(import.meta.env.VITE_WEBSOCKET_URL || 'ws://localhost:3000')
  
  socket.on('stats_update', (data) => {
    activeSessions.value = data.activeSessions
    contentViews.value = data.contentViews
  })
  
  socket.on('disconnect', () => {
    console.log('Disconnected from real-time updates')
  })
}

onMounted(async () => {
  try {
    // Simulate API calls
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Set mock statistics
    totalUsers.value = 1247
    totalContent.value = 856
    activeSessions.value = 42
    newUsersToday.value = 15
    contentViews.value = 3567
    
    // Generate mock chart data
    const userActivity = generateMockData()
    const contentMetrics = generateMockData()
    
    userActivityData.value.labels = userActivity.labels
    userActivityData.value.datasets[0].data = userActivity.data
    
    contentMetricsData.value.labels = contentMetrics.labels
    contentMetricsData.value.datasets[0].data = contentMetrics.data
    
    // Initialize real-time updates
    initializeRealTimeUpdates()
    
    isLoading.value = false
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  }
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-white">Admin Dashboard</h1>
      <div class="flex items-center space-x-4">
        <span class="text-sm text-gray-400">Last updated: {{ new Date().toLocaleTimeString() }}</span>
        <button class="btn btn-ghost text-sm" @click="initializeRealTimeUpdates">
          Refresh
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <div v-else class="space-y-6">
      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="glass-panel p-6">
          <h3 class="text-gray-400 text-sm font-medium mb-2">Total Users</h3>
          <div class="flex items-center">
            <span class="text-2xl font-bold text-white">{{ totalUsers }}</span>
            <span class="ml-2 text-sm text-success-400">+{{ newUsersToday }} today</span>
          </div>
        </div>

        <div class="glass-panel p-6">
          <h3 class="text-gray-400 text-sm font-medium mb-2">Total Content</h3>
          <div class="flex items-center">
            <span class="text-2xl font-bold text-white">{{ totalContent }}</span>
            <span class="ml-2 text-sm text-gray-400">items</span>
          </div>
        </div>

        <div class="glass-panel p-6">
          <h3 class="text-gray-400 text-sm font-medium mb-2">Active Sessions</h3>
          <div class="flex items-center">
            <span class="text-2xl font-bold text-white">{{ activeSessions }}</span>
            <span class="ml-2 text-sm text-accent-400">online now</span>
          </div>
        </div>

        <div class="glass-panel p-6">
          <h3 class="text-gray-400 text-sm font-medium mb-2">Content Views</h3>
          <div class="flex items-center">
            <span class="text-2xl font-bold text-white">{{ contentViews }}</span>
            <span class="ml-2 text-sm text-gray-400">today</span>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-panel p-6">
          <h3 class="text-lg font-semibold text-white mb-4">User Activity</h3>
          <div class="h-64">
            <Line 
              :data="userActivityData"
              :options="chartOptions"
            />
          </div>
        </div>

        <div class="glass-panel p-6">
          <h3 class="text-lg font-semibold text-white mb-4">Content Metrics</h3>
          <div class="h-64">
            <Line 
              :data="contentMetricsData"
              :options="chartOptions"
            />
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link to="/admin/content" class="glass-panel p-6 hover:bg-dark-700 transition-colors">
          <h3 class="text-lg font-semibold text-white mb-2">Content Management</h3>
          <p class="text-gray-400 text-sm">Add, edit, or remove movies and series</p>
        </router-link>

        <router-link to="/admin/users" class="glass-panel p-6 hover:bg-dark-700 transition-colors">
          <h3 class="text-lg font-semibold text-white mb-2">User Management</h3>
          <p class="text-gray-400 text-sm">Manage user accounts and permissions</p>
        </router-link>

        <div class="glass-panel p-6">
          <h3 class="text-lg font-semibold text-white mb-2">System Health</h3>
          <div class="flex items-center text-success-400">
            <span class="h-2 w-2 rounded-full bg-success-400 mr-2"></span>
            All systems operational
          </div>
        </div>
      </div>
    </div>
  </div>
</template>