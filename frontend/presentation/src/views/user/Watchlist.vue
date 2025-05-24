<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useContentStore } from '../../stores/contentStore'
import ContentCard from '../../components/ui/ContentCard.vue'

const contentStore = useContentStore()

// State
const isLoading = ref(true)
const watchlist = ref<(Movie | Series)[]>([]) // Initialize as empty array with proper type
const activeFilter = ref('all')

// Fetch watchlist on component mount
onMounted(async () => {
  try {
    await contentStore.fetchWatchlist()
    watchlist.value = contentStore.watchlist
  } catch (e) {
    console.error('Failed to load watchlist', e)
    watchlist.value = [] // Ensure watchlist is an array even on error
  } finally {
    isLoading.value = false
  }
})

// Filter watchlist with safety checks
const filteredWatchlist = computed(() => {
  // Ensure watchlist is an array before filtering
  if (!Array.isArray(watchlist.value)) {
    return []
  }

  if (activeFilter.value === 'all') {
    return watchlist.value
  } else if (activeFilter.value === 'movies') {
    return watchlist.value.filter(item => item && typeof item === 'object' && 'title' in item)
  } else if (activeFilter.value === 'series') {
    return watchlist.value.filter(item => item && typeof item === 'object' && 'name' in item)
  }
  return watchlist.value
})

function setFilter(filter: string) {
  activeFilter.value = filter
}

// Remove item from watchlist
async function removeFromWatchlist(id: number, type: 'movie' | 'series') {
  try {
    await contentStore.removeFromWatchlist(id, type)
    watchlist.value = contentStore.watchlist
  } catch (e) {
    console.error('Failed to remove from watchlist', e)
  }
}
</script>

<template>
  <div>
    <header class="mb-8">
      <h1 class="text-3xl font-bold text-white">My Watchlist</h1>
      <p class="text-gray-400">Manage your saved movies and series</p>
    </header>
    
    <!-- Filter Tabs -->
    <div class="flex border-b border-gray-800 mb-8">
      <button 
        @click="setFilter('all')"
        :class="[
          'px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors',
          activeFilter === 'all' 
            ? 'text-primary-400 border-primary-400' 
            : 'text-gray-400 border-transparent hover:text-gray-300'
        ]"
      >
        All
      </button>
      <button 
        @click="setFilter('movies')"
        :class="[
          'px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors',
          activeFilter === 'movies' 
            ? 'text-primary-400 border-primary-400' 
            : 'text-gray-400 border-transparent hover:text-gray-300'
        ]"
      >
        Movies
      </button>
      <button 
        @click="setFilter('series')"
        :class="[
          'px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors',
          activeFilter === 'series' 
            ? 'text-primary-400 border-primary-400' 
            : 'text-gray-400 border-transparent hover:text-gray-300'
        ]"
      >
        Series
      </button>
    </div>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="filteredWatchlist.length === 0" class="glass-panel p-8 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
      </svg>
      <h3 class="text-xl font-medium text-white mb-2">Your watchlist is empty</h3>
      <p class="text-gray-400 mb-6">Start adding movies and series to your watchlist</p>
      <router-link to="/" class="btn btn-primary">
        Discover Content
      </router-link>
    </div>
    
    <!-- Watchlist Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <ContentCard 
        v-for="item in filteredWatchlist" 
        :key="item.id" 
        :item="item" 
        :contentType="item && typeof item === 'object' && 'title' in item ? 'movie' : 'series'"
      />
    </div>
  </div>
</template>