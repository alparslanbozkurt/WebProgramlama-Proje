<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ContentCard from '../ui/ContentCard.vue'

type Recommendation = {
  id: number
  title: string
  type: 'movie' | 'series'
}

const suggestions = ref<Recommendation[]>([])
const isLoading = ref(false)
const aiResponse = ref('')
const userPreferences = ref('')
const router = useRouter()

// CSRF token'ı cookie'den al
function getCSRFToken(): string {
  const match = document.cookie.match(/csrftoken=([^;]+)/)
  return match ? match[1] : ''
}

async function getAiSuggestions() {
  isLoading.value = true
  aiResponse.value = ''
  suggestions.value = []

  try {
    const response = await fetch('/api/ai_recommendations/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      credentials: 'include',
      body: JSON.stringify({ preference: userPreferences.value })
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const data = await response.json()
    aiResponse.value = data.ai_summary
    suggestions.value = data.recommendations
  } catch (error) {
    aiResponse.value = 'AI önerisi alınamadı. Lütfen tercihinizi tekrar yazın.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

async function updatePreferences() {
  if (!userPreferences.value.trim()) {
    aiResponse.value = 'Lütfen tercih belirtin.'
    return
  }
  await getAiSuggestions()
}

function goToDetail(item: Recommendation) {
  const path = item.type === 'movie'
    ? `/movies/${item.id}`
    : `/tvshows/${item.id}`
  router.push(path)
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="glass-panel p-8 mb-8">
      <h1 class="text-3xl font-bold text-white mb-6">AI Movie Recommendations</h1>
      <p class="text-gray-300 mb-6">
        Get personalized movie and series recommendations powered by AI.
        Tell me about your preferences and I'll suggest content you might enjoy.
      </p>

      <div class="flex gap-4">
        <input
          v-model="userPreferences"
          type="text"
          placeholder="Tell me what kind of movies or series you enjoy (e.g., 'sci-fi with romance')"
          class="form-input flex-1"
          @keyup.enter="updatePreferences"
        />
        <button
          @click="updatePreferences"
          class="btn btn-primary whitespace-nowrap"
          :disabled="isLoading"
        >
          Get Recommendations
        </button>
      </div>
    </div>

    <!-- AI Assistant Response -->
    <div v-if="aiResponse" class="glass-panel p-6 mb-8">
      <div class="flex items-start gap-4">
        <div class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center flex-shrink-0">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-white mb-2">AI Assistant</h3>
          <p class="text-gray-300 whitespace-pre-line">{{ aiResponse }}</p>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <!-- Results -->
    <div
      v-else-if="suggestions.length > 0"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <ContentCard
        v-for="item in suggestions"
        :key="item.id"
        :item="item"
        :contentType="item.type"
        @click="goToDetail(item)"
        class="cursor-pointer"
      />
    </div>

    <!-- No Results -->
    <div v-else class="text-center py-16">
      <h3 class="text-xl font-medium text-white mb-2">No recommendations available</h3>
      <p class="text-gray-400">Try adjusting your preferences to get personalized suggestions</p>
    </div>
  </div>
</template>
