<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useContentStore } from '../../stores/contentStore'

const contentStore = useContentStore()
const isLoading = ref(true)
const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const itemsPerPage = 10
const selectedContent = ref(null)
const contentType = ref('all')

// Mock content data
const mockContent = [
  ...Array.from({ length: 30 }, (_, i) => ({
    id: i + 1,
    title: `Movie ${i + 1}`,
    type: 'movie',
    releaseDate: new Date(Date.now() - Math.random() * 300000000000).toISOString(),
    rating: (Math.random() * 5).toFixed(1),
    status: i % 5 === 0 ? 'Draft' : 'Published',
    views: Math.floor(Math.random() * 10000)
  })),
  ...Array.from({ length: 20 }, (_, i) => ({
    id: i + 31,
    title: `Series ${i + 1}`,
    type: 'series',
    releaseDate: new Date(Date.now() - Math.random() * 300000000000).toISOString(),
    rating: (Math.random() * 5).toFixed(1),
    status: i % 5 === 0 ? 'Draft' : 'Published',
    views: Math.floor(Math.random() * 10000)
  }))
]

// Filter content based on search query and type
const filteredContent = computed(() => {
  return mockContent.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesType = contentType.value === 'all' || item.type === contentType.value
    return matchesSearch && matchesType
  })
})

// Paginated content
const paginatedContent = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredContent.value.slice(start, end)
})

// Update total pages when filtered content changes
watch([filteredContent, contentType], () => {
  totalPages.value = Math.ceil(filteredContent.value.length / itemsPerPage)
  currentPage.value = 1
})

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function selectContent(content) {
  selectedContent.value = content
}

onMounted(async () => {
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    totalPages.value = Math.ceil(mockContent.length / itemsPerPage)
    isLoading.value = false
  } catch (error) {
    console.error('Failed to load content:', error)
  }
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-white">Content Management</h1>
      <button class="btn btn-primary">
        Add New Content
      </button>
    </div>

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
            placeholder="Search content..."
            class="form-input w-full"
          />
        </div>
        <div class="flex space-x-2">
          <button 
            @click="contentType = 'all'"
            class="btn"
            :class="contentType === 'all' ? 'btn-primary' : 'btn-ghost'"
          >
            All
          </button>
          <button 
            @click="contentType = 'movie'"
            class="btn"
            :class="contentType === 'movie' ? 'btn-primary' : 'btn-ghost'"
          >
            Movies
          </button>
          <button 
            @click="contentType = 'series'"
            class="btn"
            :class="contentType === 'series' ? 'btn-primary' : 'btn-ghost'"
          >
            Series
          </button>
        </div>
      </div>

      <!-- Content Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="text-left border-b border-gray-800">
              <th class="pb-3 text-gray-400 font-medium">Title</th>
              <th class="pb-3 text-gray-400 font-medium">Type</th>
              <th class="pb-3 text-gray-400 font-medium">Release Date</th>
              <th class="pb-3 text-gray-400 font-medium">Rating</th>
              <th class="pb-3 text-gray-400 font-medium">Views</th>
              <th class="pb-3 text-gray-400 font-medium">Status</th>
              <th class="pb-3 text-gray-400 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="content in paginatedContent" :key="content.id" class="border-b border-gray-800">
              <td class="py-4 text-white">{{ content.title }}</td>
              <td class="py-4">
                <span 
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    content.type === 'movie' ? 'bg-accent-900 text-accent-300' : 'bg-secondary-900 text-secondary-300'
                  ]"
                >
                  {{ content.type.charAt(0).toUpperCase() + content.type.slice(1) }}
                </span>
              </td>
              <td class="py-4 text-gray-300">{{ formatDate(content.releaseDate) }}</td>
              <td class="py-4">
                <div class="flex items-center text-yellow-400">
                  <span>{{ content.rating }}</span>
                  <svg class="h-4 w-4 ml-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
              </td>
              <td class="py-4 text-gray-300">{{ content.views.toLocaleString() }}</td>
              <td class="py-4">
                <span 
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    content.status === 'Published' ? 'bg-success-900 text-success-300' : 'bg-warning-900 text-warning-300'
                  ]"
                >
                  {{ content.status }}
                </span>
              </td>
              <td class="py-4">
                <button 
                  @click="selectContent(content)"
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
          {{ Math.min(currentPage * itemsPerPage, filteredContent.length) }} of 
          {{ filteredContent.length }} items
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