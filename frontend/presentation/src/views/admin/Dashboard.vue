<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/adminStore'

const adminStore = useAdminStore()

const isLoading = ref(true)
const stats = ref({
  totalUsers: 0,
  totalContent: 0,
  activeUsers: 0,
  pendingReviews: 0,
  pendingSuggestions: 0
})

onMounted(async () => {
  try {
    const data = await adminStore.fetchDashboardStats()
    if (data) {
      stats.value = {
        ...stats.value,
        totalUsers: data.totalUsers,
        totalContent: data.totalContent,
        activeUsers: data.activeSessions,
        pendingReviews: Math.floor(Math.random() * 10),
        pendingSuggestions: Math.floor(Math.random() * 10)
      }
    }
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-white">Admin Dashboard</h1>
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
          <div class="text-2xl font-bold text-white">{{ stats.totalUsers }}</div>
        </div>

        <div class="glass-panel p-6">
          <h3 class="text-gray-400 text-sm font-medium mb-2">Total Content</h3>
          <div class="text-2xl font-bold text-white">{{ stats.totalContent }}</div>
        </div>

        <div class="glass-panel p-6">
          <h3 class="text-gray-400 text-sm font-medium mb-2">Active Users</h3>
          <div class="text-2xl font-bold text-white">{{ stats.activeUsers }}</div>
        </div>

        <div class="glass-panel p-6">
          <h3 class="text-gray-400 text-sm font-medium mb-2">Pending Reviews</h3>
          <div class="text-2xl font-bold text-white">{{ stats.pendingReviews }}</div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link to="/admin/content" class="glass-panel p-6 hover:bg-dark-700 transition-colors">
          <h3 class="text-lg font-semibold text-white mb-2">Content Management</h3>
          <p class="text-gray-400 text-sm">Add, edit, or remove movies and series</p>
        </router-link>

        <router-link to="/admin/suggestions" class="glass-panel p-6 hover:bg-dark-700 transition-colors">
          <h3 class="text-lg font-semibold text-white mb-2">Suggestions Management</h3>
          <p class="text-gray-400 text-sm">Review and manage content suggestions</p>
          <div v-if="stats.pendingSuggestions" class="mt-2 inline-flex items-center px-2 py-1 rounded-full bg-primary-900 text-primary-300 text-sm">
            {{ stats.pendingSuggestions }} pending
          </div>
        </router-link>

        <router-link to="/admin/reviews" class="glass-panel p-6 hover:bg-dark-700 transition-colors">
          <h3 class="text-lg font-semibold text-white mb-2">Review Management</h3>
          <p class="text-gray-400 text-sm">Moderate user reviews and comments</p>
          <div v-if="stats.pendingReviews" class="mt-2 inline-flex items-center px-2 py-1 rounded-full bg-primary-900 text-primary-300 text-sm">
            {{ stats.pendingReviews }} pending
          </div>
        </router-link>

        <router-link to="/admin/users" class="glass-panel p-6 hover:bg-dark-700 transition-colors">
          <h3 class="text-lg font-semibold text-white mb-2">User Management</h3>
          <p class="text-gray-400 text-sm">Manage user accounts and permissions</p>
        </router-link>
      </div>
    </div>
  </div>
</template>