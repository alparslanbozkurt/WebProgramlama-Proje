<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useContentStore } from '../../stores/contentStore'
import  ContentCard from '../ui/ContentCard.vue'
import type { Movie, Series } from '../../stores/contentStore'

const contentStore = useContentStore()
const suggestions = ref<(Movie | Series)[]>([])
const isLoading = ref(true)

onMounted(async () => {
  try {
    await contentStore.fetchRecommendations()
    suggestions.value = contentStore.recommendations
  } catch (error) {
    console.error('Failed to fetch suggestions:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="glass-panel p-6 rounded-lg">
    <h2 class="text-xl font-semibold text-white mb-6">Recommended for You</h2>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-500"></div>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="suggestions.length === 0" class="text-center py-8">
      <p class="text-gray-400">No recommendations available yet. Start watching movies to get personalized suggestions!</p>
    </div>
    
    <!-- Suggestions Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <ContentCard 
        v-for="item in suggestions" 
        :key="item.id" 
        :item="item" 
        :contentType="'title' in item ? 'movie' : 'series'"
      />
    </div>
  </div>
</template>