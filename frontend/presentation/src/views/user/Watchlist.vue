<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useContentStore } from '../../stores/contentStore'
import type { Movie, Series } from '../../stores/contentStore'
import ContentCard from '../../components/ui/ContentCard.vue'

const contentStore = useContentStore()

// State
const isLoading = ref(true)
const watchlist = ref<(Movie | Series)[]>([])
const activeFilter = ref('all')

// Fetch watchlist on component mount
onMounted(async () => {
  try {
    await contentStore.fetchWatchlist()
    watchlist.value = contentStore.watchlist
  } catch (e) {
    console.error('Failed to load watchlist', e)
    watchlist.value = []
  } finally {
    isLoading.value = false
  }
})

// Filter watchlist with safety checks
const filteredWatchlist = computed(() => {
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
async function removeFromWatchlist(id: number) {
  try {
    await contentStore.removeFromWatchlist(id)
    watchlist.value = contentStore.watchlist
  } catch (e) {
    console.error('Failed to remove from watchlist', e)
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-white mb-6">My Watchlist</h1>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <div v-else>
      <!-- Filter Tabs -->
      <div class="flex border-b border-gray-800 mb-8">
        <button 
          v-for="filter in ['all', 'movies', 'series']"
          :key="filter"
          @click="setFilter(filter)"
          class="px-6 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors"
          :class="activeFilter === filter 
            ? 'text-primary-400 border-primary-400' 
            : 'text-gray-400 border-transparent hover:text-gray-300'"
        >
          {{ filter.charAt(0).toUpperCase() + filter.slice(1) }}
        </button>
      </div>

      <!-- Watchlist Grid -->
      <div v-if="filteredWatchlist.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <ContentCard 
          v-for="item in filteredWatchlist" 
          :key="item.id" 
          :item="item" 
          :contentType="'title' in item ? 'movie' : 'series'"
          @remove="removeFromWatchlist(item.id)"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <h3 class="text-xl font-medium text-white mb-2">Your watchlist is empty</h3>
        <p class="text-gray-400 mb-6">Start adding movies and series to your watchlist</p>
        <router-link to="/" class="btn btn-primary">
          Discover Content
        </router-link>
      </div>
    </div>
  </div>
</template>