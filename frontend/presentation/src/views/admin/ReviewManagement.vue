<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAdminStore } from '../../stores/adminStore'
import { toast } from 'vue3-toastify'

const adminStore = useAdminStore()

// State
const isLoading = ref(true)
const reviews = ref([])
const selectedReview = ref(null)
const searchQuery = ref('')
const filterStatus = ref('all')
const currentPage = ref(1)
const itemsPerPage = 10
const showDeleteModal = ref(false)

// Mock reviews data
const mockReviews = Array.from({ length: 50 }, (_, i) => ({
  id: i + 1,
  userId: i + 1,
  username: `user${i + 1}`,
  contentId: Math.floor(Math.random() * 20) + 1,
  contentTitle: `Content ${Math.floor(Math.random() * 20) + 1}`,
  contentType: Math.random() > 0.5 ? 'movie' : 'series',
  rating: Math.floor(Math.random() * 5) + 1,
  comment: `This is a ${i % 3 === 0 ? 'great' : i % 3 === 1 ? 'good' : 'amazing'} ${Math.random() > 0.5 ? 'movie' : 'series'}! ${i % 2 === 0 ? 'Highly recommended!' : 'Worth watching.'}`,
  status: i % 10 === 0 ? 'reported' : 'approved',
  createdAt: new Date(Date.now() - Math.random() * 30000000000).toISOString()
}))

// Filtered reviews
const filteredReviews = computed(() => {
  let filtered = [...reviews.value]
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(review => 
      review.username.toLowerCase().includes(query) ||
      review.contentTitle.toLowerCase().includes(query) ||
      review.comment.toLowerCase().includes(query)
    )
  }
  
  if (filterStatus.value !== 'all') {
    filtered = filtered.filter(review => review.status === filterStatus.value)
  }
  
  return filtered
})

// Paginated reviews
const paginatedReviews = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredReviews.value.slice(start, end)
})

const totalPages = computed(() => 
  Math.ceil(filteredReviews.value.length / itemsPerPage)
)

// Methods
async function loadReviews() {
  try {
    // In a real app, this would be an API call
    reviews.value = mockReviews
  } catch (error) {
    toast.error('Failed to load reviews')
  } finally {
    isLoading.value = false
  }
}

async function approveReview(review) {
  try {
    review.status = 'approved'
    toast.success('Review approved')
  } catch (error) {
    toast.error('Failed to approve review')
  }
}

async function rejectReview(review) {
  try {
    review.status = 'rejected'
    toast.success('Review rejected')
  } catch (error) {
    toast.error('Failed to reject review')
  }
}

async function deleteReview() {
  try {
    reviews.value = reviews.value.filter(r => r.id !== selectedReview.value.id)
    showDeleteModal.value = false
    selectedReview.value = null
    toast.success('Review deleted')
  } catch (error) {
    toast.error('Failed to delete review')
  }
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(loadReviews)
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-white mb-8">Review Management</h1>

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
            placeholder="Search reviews..."
            class="form-input w-full"
          />
        </div>
        <div class="flex space-x-2">
          <button 
            v-for="status in ['all', 'reported', 'approved', 'rejected']"
            :key="status"
            @click="filterStatus = status"
            class="btn"
            :class="filterStatus === status ? 'btn-primary' : 'btn-ghost'"
          >
            {{ status.charAt(0).toUpperCase() + status.slice(1) }}
          </button>
        </div>
      </div>

      <!-- Reviews Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="text-left border-b border-gray-800">
              <th class="pb-3 text-gray-400 font-medium">User</th>
              <th class="pb-3 text-gray-400 font-medium">Content</th>
              <th class="pb-3 text-gray-400 font-medium">Rating</th>
              <th class="pb-3 text-gray-400 font-medium">Comment</th>
              <th class="pb-3 text-gray-400 font-medium">Status</th>
              <th class="pb-3 text-gray-400 font-medium">Date</th>
              <th class="pb-3 text-gray-400 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="review in paginatedReviews" :key="review.id" class="border-b border-gray-800">
              <td class="py-4 text-white">{{ review.username }}</td>
              <td class="py-4">
                <div>
                  <span class="text-white">{{ review.contentTitle }}</span>
                  <span 
                    :class="[
                      'ml-2 px-2 py-1 text-xs rounded-full',
                      review.contentType === 'movie' ? 'bg-accent-900 text-accent-300' : 'bg-secondary-900 text-secondary-300'
                    ]"
                  >
                    {{ review.contentType }}
                  </span>
                </div>
              </td>
              <td class="py-4">
                <div class="flex items-center text-yellow-400">
                  <span>{{ review.rating }}/5</span>
                </div>
              </td>
              <td class="py-4 text-gray-300">
                <div class="max-w-xs truncate">{{ review.comment }}</div>
              </td>
              <td class="py-4">
                <span
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    review.status === 'approved' ? 'bg-success-900 text-success-300' :
                    review.status === 'rejected' ? 'bg-error-900 text-error-300' :
                    'bg-warning-900 text-warning-300'
                  ]"
                >
                  {{ review.status.charAt(0).toUpperCase() + review.status.slice(1) }}
                </span>
              </td>
              <td class="py-4 text-gray-300">{{ formatDate(review.createdAt) }}</td>
              <td class="py-4">
                <div class="flex space-x-2">
                  <button 
                    v-if="review.status !== 'approved'"
                    @click="approveReview(review)"
                    class="text-success-400 hover:text-success-300"
                  >
                    Approve
                  </button>
                  <button 
                    v-if="review.status !== 'rejected'"
                    @click="rejectReview(review)"
                    class="text-warning-400 hover:text-warning-300"
                  >
                    Reject
                  </button>
                  <button 
                    @click="(showDeleteModal = true, selectedReview = review)"
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
          {{ Math.min(currentPage * itemsPerPage, filteredReviews.length) }} of 
          {{ filteredReviews.length }} reviews
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

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="glass-panel p-6 rounded-lg w-full max-w-md">
        <h3 class="text-xl font-semibold text-white mb-4">Delete Review</h3>
        <p class="text-gray-300 mb-4">
          Are you sure you want to delete this review? This action cannot be undone.
        </p>
        <div class="flex justify-end space-x-4">
          <button @click="showDeleteModal = false" class="btn btn-ghost">Cancel</button>
          <button 
            @click="deleteReview"
            class="btn btn-error"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>