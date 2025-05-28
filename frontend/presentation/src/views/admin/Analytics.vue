<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '../../stores/authStore'
import { toast } from 'vue3-toastify'

const authStore = useAuthStore()
const isLoading = ref(true)
const users = ref([])
const selectedUser = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const itemsPerPage = 10
const showBanModal = ref(false)
const banReason = ref('')

// Mock user data
const mockUsers = Array.from({ length: 50 }, (_, i) => ({
  id: i + 1,
  username: `user${i + 1}`,
  email: `user${i + 1}@example.com`,
  role: i < 3 ? 'Admin' : 'User',
  status: i % 5 === 0 ? 'Banned' : 'Active',
  lastLogin: new Date(Date.now() - Math.random() * 10000000000).toISOString(),
  createdAt: new Date(Date.now() - Math.random() * 30000000000).toISOString(),
  banReason: i % 5 === 0 ? 'Violation of terms' : null
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

async function banUser(user) {
  try {
    // In a real app, make API call to ban user
    user.status = 'Banned'
    user.banReason = banReason.value
    showBanModal.value = false
    banReason.value = ''
    toast.success(`User ${user.username} has been banned`)
  } catch (error) {
    toast.error('Failed to ban user')
  }
}

async function unbanUser(user) {
  try {
    // In a real app, make API call to unban user
    user.status = 'Active'
    user.banReason = null
    toast.success(`User ${user.username} has been unbanned`)
  } catch (error) {
    toast.error('Failed to unban user')
  }
}

async function deleteUser(user) {
  if (!confirm(`Are you sure you want to delete user ${user.username}?`)) {
    return
  }

  try {
    // In a real app, make API call to delete user
    mockUsers.splice(mockUsers.indexOf(user), 1)
    toast.success(`User ${user.username} has been deleted`)
  } catch (error) {
    toast.error('Failed to delete user')
  }
}

async function updateUserRole(user, newRole) {
  try {
    // In a real app, make API call to update user role
    user.role = newRole
    toast.success(`User role updated to ${newRole}`)
  } catch (error) {
    toast.error('Failed to update user role')
  }
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
                <select 
                  v-if="user.id !== authStore.user?.id"
                  :value="user.role"
                  @change="updateUserRole(user, $event.target.value)"
                  class="form-input text-sm py-1"
                >
                  <option value="User">User</option>
                  <option value="Editor">Editor</option>
                  <option value="Admin">Admin</option>
                </select>
                <span v-else class="px-2 py-1 text-xs rounded-full bg-primary-900 text-primary-300">
                  {{ user.role }}
                </span>
              </td>
              <td class="py-4">
                <span 
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    user.status === 'Active' ? 'bg-success-900 text-success-300' : 'bg-error-900 text-error-300'
                  ]"
                  :title="user.banReason"
                >
                  {{ user.status }}
                </span>
              </td>
              <td class="py-4 text-gray-300">{{ formatDate(user.lastLogin) }}</td>
              <td class="py-4">
                <div class="flex space-x-2">
                  <button 
                    v-if="user.id !== authStore.user?.id"
                    @click="user.status === 'Active' ? (showBanModal = true, selectedUser = user) : unbanUser(user)"
                    :class="[
                      'text-sm px-2 py-1 rounded',
                      user.status === 'Active' ? 'text-error-400 hover:text-error-300' : 'text-success-400 hover:text-success-300'
                    ]"
                  >
                    {{ user.status === 'Active' ? 'Ban' : 'Unban' }}
                  </button>
                  <button 
                    v-if="user.id !== authStore.user?.id"
                    @click="deleteUser(user)"
                    class="text-sm px-2 py-1 rounded text-error-400 hover:text-error-300"
                  >
                    Delete
                  </button>
                </div>
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

    <!-- Ban User Modal -->
    <div v-if="showBanModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="glass-panel p-6 rounded-lg w-full max-w-md">
        <h3 class="text-xl font-semibold text-white mb-4">Ban User</h3>
        <p class="text-gray-300 mb-4">Are you sure you want to ban {{ selectedUser?.username }}?</p>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-300 mb-1">Reason for ban</label>
          <textarea
            v-model="banReason"
            rows="3"
            class="form-input w-full"
            placeholder="Enter reason for ban..."
          ></textarea>
        </div>
        <div class="flex justify-end space-x-4">
          <button @click="showBanModal = false" class="btn btn-ghost">Cancel</button>
          <button 
            @click="banUser(selectedUser)"
            class="btn btn-error"
            :disabled="!banReason.trim()"
          >
            Ban User
          </button>
        </div>
      </div>
    </div>
  </div>
</template>