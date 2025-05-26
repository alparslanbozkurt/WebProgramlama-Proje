<script setup lang="ts">
import { computed, defineProps } from 'vue'
import { useContentStore } from '../../stores/contentStore'
import { useAuthStore } from '../../stores/authStore'
import type { Movie, Series } from '../../stores/contentStore'

const props = defineProps<{
  item: Movie | Series
  contentType: 'movie' | 'series'
}>()

const contentStore = useContentStore()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

const title = computed(() =>
  props.contentType === 'movie'
    ? (props.item as Movie).title
    : (props.item as Series).name
)

const releaseDate = computed(() => {
  const date = props.contentType === 'movie'
    ? (props.item as Movie).release_date
    : (props.item as Series).first_air_date
  return date ? new Date(date).getFullYear() : ''
})

// TMDB image base URL’i .env’den oku
const TMDB_IMG_BASE = import.meta.env.VITE_TMDB_IMG_BASE as string

// poster_path’i full URL’e çevir, yoksa fallback
const posterUrl = computed<string>(() =>
  props.item.poster_path
    ? `${TMDB_IMG_BASE}${props.item.poster_path}`
    : '/fallback-poster.png'
)

// Rating’i 10’luk ölçekten 5’like dönüştür, tek ondalığa yuvarla
const rating = computed(() =>
  ((props.item.vote_average ?? 0) / 2).toFixed(1)
)

async function addToWatchlist() {
  await contentStore.addToWatchlist(props.item.id, props.contentType)
}
</script>

<template>
  <div class="card-gradient group h-full flex flex-col relative overflow-hidden transition-transform duration-300 transform hover:scale-[1.02]">
    
    <div class="absolute inset-0 bg-gradient-to-t from-dark-950 via-dark-950/70 to-transparent opacity-70"></div>
    
    
    <div class="w-full h-80 overflow-hidden relative">
      <img 
        :src="posterUrl" 
        :alt="title"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
      />
    </div>
    
    
    <div class="relative z-10 p-4 mt-auto">
      <div class="flex items-start justify-between">
        <h3 class="text-lg font-semibold text-white line-clamp-2">{{ title }}</h3>
        <span class="inline-flex items-center px-2 py-1 rounded-md bg-dark-800/70 backdrop-blur-sm text-yellow-400 text-sm font-medium">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
          {{ rating }}
        </span>
      </div>
      
      <div class="flex items-center mt-2 text-sm text-gray-300">
        <span>{{ releaseDate }}</span>
        <span class="mx-2">•</span>
        <span class="capitalize">{{ contentType }}</span>
      </div>
      
      
      <div class="flex mt-4">
        <router-link :to="`/${contentType}/${item.id}`" class="btn btn-primary flex-1 mr-2 text-center">
          Details
        </router-link>
        <button 
          v-if="isAuthenticated"
          @click="addToWatchlist"
          class="btn btn-ghost p-2 flex items-center justify-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>