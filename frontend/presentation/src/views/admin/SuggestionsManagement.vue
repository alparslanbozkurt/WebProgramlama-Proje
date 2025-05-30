<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAdminStore } from '../../stores/adminStore'
import { toast } from 'vue3-toastify'

const adminStore = useAdminStore()

// State
const isLoading = ref(true)
const suggestions = ref([])
const selectedSuggestion = ref(null)
const searchQuery = ref('')
const filterType = ref('all')
const currentPage = ref(1)
const itemsPerPage = 10
const showDeleteModal = ref(false)
const showDetailsModal = ref(false)

// Mock suggestions data
const mockSuggestions = Array.from({ length: 50 }, (_, i) => ({
  id: i + 1,
  userId: i + 1,
  username: `user${i + 1}`,
  title: `Suggested ${i % 2 === 0 ? 'Movie' : 'Series'} ${i + 1}`,
  type: i % 2 === 0 ? 'movie' : 'series',
  overview: `This is a suggestion for a ${i % 2 === 0 ? 'movie' : 'series'} that would be great for our platform.`,
  genre: ['Action', 'Drama', 'Comedy', 'Sci-Fi'][Math.floor(Math.random() * 4)],
  status: ['pending', 'approved', 'rejected'][Math.floor(Math.random() * 3)],
  reason: '',
  createdAt: new Date(Date.now() - Math.random() * 30000000000).toISOString()
}))

// Filtered suggestions
const filteredSuggestions = computed(() => {
  let filtered = [...suggestions.value]
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(suggestion => 
      suggestion.title.toLowerCase().includes(query) ||
      suggestion.username.toLowerCase().includes(query)
    )
  }
  
  if (filterType.value !== 'all') {
    filtered = filtered.filter(suggestion => suggestion.type === filterType.value)
  }
  
  return filtered
})

// Paginated suggestions
const paginatedSuggestions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredSuggestions.value.slice(start, end)
})

const totalPages = computed(() => 
  Math.ceil(filteredSuggestions.value.length / itemsPerPage)
)

// Methods
async function loadSuggestions() {
  try {
    // In a real app, this would be an API call
    suggestions.value = mockSuggestions
  } catch (error) {
    toast.error('Failed to load suggestions')
  } finally {
    isLoading.value = false
  }
}

async function approveSuggestion(suggestion) {
  try {
    suggestion.status = 'approved'
    toast.success('Suggestion approved')
  } catch (error) {
    toast.error('Failed to approve suggestion')
  }
}

async function rejectSuggestion(suggestion) {
  try {
    suggestion.status = 'rejected'
    toast.success('Suggestion rejected')
  } catch (error) {
    toast.error('Failed to reject suggestion')
  }
}

async function deleteSuggestion() {
  try {
    suggestions.value = suggestions.value.filter(s => s.id !== selectedSuggestion.value.id)
    showDeleteModal.value = false
    selectedSuggestion.value = null
    toast.success('Suggestion deleted')
  } catch (error) {
    toast.error('Failed to delete suggestion')
  }
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(loadSuggestions)
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-white mb-8">Suggestions Management</h1>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <div v-else class="glass-panel p-6">
      <!-- Search and Filters -->
      <div class="flex flex-col sm:flex-row justify-between items-center mb-6 space-y-4 sm:space-y-0">
        <div class="w-full sm:w-64">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search suggestions..."
            class="form-input w-full"
          />
        </div>
        <div class="flex space-x-2">
          <button 
            v-for="type in ['all', 'movie', 'series']"
            :key="type"
            @click="filterType = type"
            class="btn"
            :class="filterType === type ? 'btn-primary' : 'btn-ghost'"
          >
            {{ type.charAt(0).toUpperCase() + type.slice(1) }}
          </button>
        </div>
      </div>

      <!-- Suggestions Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="text-left border-b border-gray-800">
              <th class="pb-3 text-gray-400 font-medium">Title</th>
              <th class="pb-3 text-gray-400 font-medium">Type</th>
              <th class="pb-3 text-gray-400 font-medium">Suggested By</th>
              <th class="pb-3 text-gray-400 font-medium">Genre</th>
              <th class="pb-3 text-gray-400 font-medium">Status</th>
              <th class="pb-3 text-gray-400 font-medium">Date</th>
              <th class="pb-3 text-gray-400 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="suggestion in paginatedSuggestions" :key="suggestion.id" class="border-b border-gray-800">
              <td class="py-4 text-white">{{ suggestion.title }}</td>
              <td class="py-4">
                <span 
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    suggestion.type === 'movie' ? 'bg-accent-900 text-accent-300' : 'bg-secondary-900 text-secondary-300'
                  ]"
                >
                  {{ suggestion.type.charAt(0).toUpperCase() + suggestion.type.slice(1) }}
                </span>
              </td>
              <td class="py-4 text-gray-300">{{ suggestion.username }}</td>
              <td class="py-4">
                <span class="px-2 py-1 text-xs rounded-full bg-dark-700 text-gray-300">
                  {{ suggestion.genre }}
                </span>
              </td>
              <td class="py-4">
                <span
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    suggestion.status === 'approved' ? 'bg-success-900 text-success-300' :
                    suggestion.status === 'rejected' ? 'bg-error-900 text-error-300' :
                    'bg-warning-900 text-warning-300'
                  ]"
                >
                  {{ suggestion.status.charAt(0).toUpperCase() + suggestion.status.slice(1) }}
                </span>
              </td>
              <td class="py-4 text-gray-300">{{ formatDate(suggestion.createdAt) }}</td>
              <td class="py-4">
                <div class="flex space-x-2">
                  <button 
                    @click="(showDetailsModal = true, selectedSuggestion = suggestion)"
                    class="text-primary-400 hover:text-primary-300"
                  >
                    Details
                  </button>
                  <button 
                    v-if="suggestion.status === 'pending'"
                    @click="approveSuggestion(suggestion)"
                    class="text-success-400 hover:text-success-300"
                  >
                    Approve
                  </button>
                  <button 
                    v-if="suggestion.status === 'pending'"
                    @click="rejectSuggestion(suggestion)"
                    class="text-warning-400 hover:text-warning-300"
                  >
                    Reject
                  </button>
                  <button 
                    @click="(showDeleteModal = true, selectedSuggestion = suggestion)"
                    class="text-error-400 hover:text-error-300"
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
          {{ Math.min(currentPage * itemsPerPage, filteredSuggestions.length) }} of 
          {{ filteredSuggestions.length }} suggestions
        </div>
        <div class="flex space-x-2">
          <button 
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="btn btn-ghost"
            :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
          >
            Previous
          </button>
          <button 
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="btn btn-ghost"
            :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="glass-panel p-6 rounded-lg w-full max-w-2xl">
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-xl font-semibold text-white">Suggestion Details</h3>
          <button 
            @click="showDetailsModal = false"
            class="text-gray-400 hover:text-white"
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-4">
          <div>
            <h4 class="text-sm font-medium text-gray-400">Title</h4>
            <p class="text-white">{{ selectedSuggestion?.title }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-400">Overview</h4>
            <p class="text-gray-300">{{ selectedSuggestion?.overview }}</p>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-400">Type</h4>
              <p class="text-white capitalize">{{ selectedSuggestion?.type }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-400">Genre</h4>
              <p class="text-white">{{ selectedSuggestion?.genre }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-400">Suggested By</h4>
              <p class="text-white">{{ selectedSuggestion?.username }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-400">Date</h4>
              <p class="text-white">{{ formatDate(selectedSuggestion?.createdAt) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="glass-panel p-6 rounded-lg w-full max-w-md">
        <h3 class="text-xl font-semibold text-white mb-4">Delete Suggestion</h3>
        <p class="text-gray-300 mb-4">
          Are you sure you want to delete this suggestion? This action cannot be undone.
        </p>
        <div class="flex justify-end space-x-4">
          <button @click="showDeleteModal = false" class="btn btn-ghost">Cancel</button>
          <button 
            @click="deleteSuggestion"
            class="btn btn-error"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>