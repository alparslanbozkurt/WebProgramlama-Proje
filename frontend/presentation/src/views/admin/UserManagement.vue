<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '../../stores/authStore'

const authStore = useAuthStore()
const isLoading = ref(true)
const users = ref([])
const selectedUser = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const itemsPerPage = 10

// Mock user data
const mockUsers = Array.from({ length: 50 }, (_, i) => ({
  id: i + 1,
  username: `user${i + 1}`,
  email: `user${i + 1}@example.com`,
  role: i < 3 ? 'Admin' : 'User',
  status: i % 5 === 0 ? 'Inactive' : 'Active',
  lastLogin: new Date(Date.now() - Math.random() * 10000000000).toISOString(),
  createdAt: new Date(Date.now() - Math.random() * 30000000000).toISOString()
}))

// Filter users based on search query
const filteredUsers = computed(() => {
  return mockUsers.filter(user => 
    user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Paginated users
const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredUsers.value.slice(start, end)
})

// Update total pages when filtered users change
watch(filteredUsers, () => {
  totalPages.value = Math.ceil(filteredUsers.value.length / itemsPerPage)
  currentPage.value = 1
})

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function selectUser(user) {
  selectedUser.value = user
}

onMounted(async () => {
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    users.value = mockUsers
    totalPages.value = Math.ceil(mockUsers.length / itemsPerPage)
    isLoading.value = false
  } catch (error) {
    console.error('Failed to load users:', error)
  }
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-white">User Management</h1>
      <button class="btn btn-primary">
        Add New User
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <div v-else class="glass-panel p-6">
      <!-- Search and Filters -->
      <div class="flex flex-col sm:flex-row justify-between items-center mb-6">
        <div class="w-full sm:w-64 mb-4 sm:mb-0">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search users..."
            class="form-input w-full"
          />
        </div>
      </div>

      <!-- Users Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="text-left border-b border-gray-800">
              <th class="pb-3 text-gray-400 font-medium">Username</th>
              <th class="pb-3 text-gray-400 font-medium">Email</th>
              <th class="pb-3 text-gray-400 font-medium">Role</th>
              <th class="pb-3 text-gray-400 font-medium">Status</th>
              <th class="pb-3 text-gray-400 font-medium">Last Login</th>
              <th class="pb-3 text-gray-400 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id" class="border-b border-gray-800">
              <td class="py-4 text-white">{{ user.username }}</td>
              <td class="py-4 text-gray-300">{{ user.email }}</td>
              <td class="py-4">
                <span 
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    user.role === 'Admin' ? 'bg-primary-900 text-primary-300' : 'bg-gray-800 text-gray-300'
                  ]"
                >
                  {{ user.role }}
                </span>
              </td>
              <td class="py-4">
                <span 
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    user.status === 'Active' ? 'bg-success-900 text-success-300' : 'bg-error-900 text-error-300'
                  ]"
                >
                  {{ user.status }}
                </span>
              </td>
              <td class="py-4 text-gray-300">{{ formatDate(user.lastLogin) }}</td>
              <td class="py-4">
                <button 
                  @click="selectUser(user)"
                  class="text-primary-400 hover:text-primary-300 mr-3"
                >
                  Edit
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-6">
        <div class="text-sm text-gray-400">
          Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to 
          {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }} of 
          {{ filteredUsers.length }} users
        </div>
        <div class="flex space-x-2">
          <button 
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="btn btn-ghost text-sm"
            :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
          >
            Previous
          </button>
          <button 
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="btn btn-ghost text-sm"
            :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>