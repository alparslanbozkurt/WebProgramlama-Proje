<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useContentStore } from '../../stores/contentStore'
import ContentCard from '../../components/ui/ContentCard.vue'

const contentStore = useContentStore()
const isLoading = ref(true)
const movies = ref([])
const currentPage = ref(1)
const itemsPerPage = 12
const searchQuery = ref('')
const selectedGenre = ref('all')

// Computed properties would be more efficient, but keeping it simple for demo
const filteredMovies = ref([])

onMounted(async () => {
  try {
    await contentStore.fetchTrending()
    movies.value = contentStore.trendingMovies
    updateFilteredMovies()
  } catch (error) {
    console.error('Failed to fetch movies:', error)
  } finally {
    isLoading.value = false
  }
})

function updateFilteredMovies() {
  let filtered = [...movies.value]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(movie => 
      movie.title.toLowerCase().includes(query) ||
      movie.overview.toLowerCase().includes(query)
    )
  }
  
  // Apply genre filter
  if (selectedGenre.value !== 'all') {
    filtered = filtered.filter(movie => 
      movie.genres.includes(selectedGenre.value)
    )
  }
  
  filteredMovies.value = filtered
}

function handleSearch() {
  currentPage.value = 1
  updateFilteredMovies()
}

const genres = [
  'Action', 'Adventure', 'Comedy', 'Drama', 'Horror', 
  'Romance', 'Sci-Fi', 'Thriller'
]

const paginatedMovies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredMovies.value.slice(start, end)
})

const totalPages = computed(() => 
  Math.ceil(filteredMovies.value.length / itemsPerPage)
)
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-white mb-8">All Movies</h1>

    <!-- Filters -->
    <div class="glass-panel p-6 mb-8">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1">
          <input
            type="text"
            v-model="searchQuery"
            @input="handleSearch"
            placeholder="Search movies..."
            class="form-input w-full"
          />
        </div>

        <!-- Genre Filter -->
        <div class="w-full md:w-48">
          <select
            v-model="selectedGenre"
            @change="handleSearch"
            class="form-input w-full"
          >
            <option value="all">All Genres</option>
            <option v-for="genre in genres" :key="genre" :value="genre">
              {{ genre }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <!-- No Results -->
    <div v-else-if="filteredMovies.length === 0" class="text-center py-16">
      <h3 class="text-xl font-medium text-white mb-2">No movies found</h3>
      <p class="text-gray-400">Try adjusting your search criteria</p>
    </div>

    <!-- Movies Grid -->
    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <ContentCard
          v-for="movie in paginatedMovies"
          :key="movie.id"
          :item="movie"
          contentType="movie"
        />
      </div>

      <!-- Pagination -->
      <div class="flex justify-center mt-8 space-x-2">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="btn btn-ghost"
          :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
        >
          Previous
        </button>
        <span class="flex items-center px-4 text-gray-400">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
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
</template>