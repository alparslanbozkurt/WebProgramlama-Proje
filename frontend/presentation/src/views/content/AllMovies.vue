<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useContentStore } from '../../stores/contentStore'
import ContentCard from '../../components/ui/ContentCard.vue'

const contentStore = useContentStore()

const isLoading = ref(true)
const movies = ref<typeof contentStore.trendingMovies>([])
const currentPage = ref(1)
const itemsPerPage = 12

const searchQuery = ref('')
const selectedGenre = ref('all')
const filteredMovies = ref<typeof movies.value>([])

// Sayfa açıldığında önce hem filmleri hem de tür listesini çek
onMounted(async () => {
  isLoading.value = true
  await Promise.all([
    contentStore.fetchTrending(),
    contentStore.fetchGenres()
  ])
  movies.value = contentStore.trendingMovies
  updateFilteredMovies()
  isLoading.value = false
})

function updateFilteredMovies() {
  let temp = [...movies.value]

  // arama
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    temp = temp.filter(m =>
      m.title.toLowerCase().includes(q) ||
      m.overview.toLowerCase().includes(q)
    )
  }

  // tür filtresi
  if (selectedGenre.value !== 'all') {
    temp = temp.filter(m =>
      m.genres?.includes(selectedGenre.value)
    )
  }

  filteredMovies.value = temp
}

function handleSearch() {
  currentPage.value = 1
  updateFilteredMovies()
}

const genres = computed(() => [
  { label: 'All Genres', value: 'all' },
  ...contentStore.genres.map(g => ({ label: g, value: g }))
])

const paginatedMovies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredMovies.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() =>
  Math.ceil(filteredMovies.value.length / itemsPerPage)
)
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-white mb-8">All Movies</h1>

    <!-- Filtre paneli -->
    <div class="glass-panel p-6 mb-8">
      <div class="flex flex-col md:flex-row gap-4">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          placeholder="Search movies…"
          class="form-input flex-1"
        />
        <select
          v-model="selectedGenre"
          @change="handleSearch"
          class="form-input w-full md:w-48"
        >
          <option
            v-for="opt in genres"
            :key="opt.value"
            :value="opt.value"
          >
            {{ opt.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="flex justify-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <!-- Sonuç yok -->
    <div v-else-if="filteredMovies.length === 0" class="text-center py-16">
      <h3 class="text-xl text-white mb-2">No movies found</h3>
      <p class="text-gray-400">Try adjusting your filters</p>
    </div>

    <!-- Film kartları -->
    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <ContentCard
          v-for="movie in paginatedMovies"
          :key="movie.id"
          :item="movie"
          contentType="movie"
        />
      </div>

      <!-- Sayfalama -->
      <div class="flex justify-center mt-8 space-x-2">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="btn btn-ghost"
        >
          Previous
        </button>
        <span class="flex items-center text-gray-400">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="btn btn-ghost"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
