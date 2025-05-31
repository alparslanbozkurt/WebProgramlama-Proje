<template>
  <div>
    <!-- Hero Section -->
    <section class="relative overflow-hidden mb-12 -mx-4 mt-[-4rem] pt-24 pb-16">
      <div class="absolute inset-0 bg-dark-950 overflow-hidden">
        <div class="absolute inset-0 bg-gradient-radial from-primary-900/20 to-dark-950"></div>
        <div class="absolute top-0 left-0 right-0 h-[50%] bg-gradient-to-b from-dark-900 to-transparent"></div>
        <div
          class="absolute inset-0 bg-[url('https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')] bg-cover bg-center opacity-10"
        ></div>
      </div>

      <div class="container mx-auto px-4 relative z-10">
        <div class="max-w-3xl">
          <h1 class="text-5xl font-bold text-white mb-4 leading-tight">
            Your <span class="text-accent-400 text-shadow">Personalized</span> Movie Experience
          </h1>
          <p class="text-xl text-gray-300 mb-8">
            Discover movies and series tailored to your unique preferences through our advanced AI recommendation system.
          </p>
          <div class="flex flex-wrap gap-4">
            <router-link
              v-if="!authStore.isAuthenticated"
              to="/register"
              class="btn btn-primary px-6 py-3"
            >
              Get Started
            </router-link>
            <a href="#trending" class="btn btn-ghost px-6 py-3">
              Explore Trending
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <!-- Main Content -->
    <div v-else>
      <!-- Recommendations Section -->
      <section
        v-if="authStore.isAuthenticated && recommendations.length > 0"
        class="mb-12"
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-white">Recommended For You</h2>
          <router-link
            to="/recommendations"
            class="text-primary-400 hover:text-primary-300 transition-colors text-sm"
          >
            View All
          </router-link>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <ContentCard
            v-for="item in recommendations.filter(i => i && typeof i === 'object')"
            :key="item.id"
            :item="item"
            :contentType="getContentType(item)"
          />
        </div>
      </section>

      <!-- Trending Movies Section -->
      <section id="trending" class="mb-12">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-white">Trending Movies</h2>
          <router-link
            to="/movies"
            class="text-primary-400 hover:text-primary-300 transition-colors text-sm"
          >
            View All
          </router-link>
        </div>

        <div v-if="trendingMovies.length === 0" class="text-center py-8 text-gray-400">
          No trending movies available at the moment.
        </div>

        <div
          v-else
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
        >
          <ContentCard
            v-for="movie in trendingMovies.slice(0, 4)"
            :key="movie.id"
            :item="movie"
            contentType="movie"
          />
        </div>
      </section>

      <!-- Trending Series Section -->
      <section class="mb-12">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-white">Trending Series</h2>
          <router-link
            to="/series"
            class="text-primary-400 hover:text-primary-300 transition-colors text-sm"
          >
            View All
          </router-link>
        </div>

        <div v-if="trendingSeries.length === 0" class="text-center py-8 text-gray-400">
          No trending series available at the moment.
        </div>

        <div
          v-else
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
        >
          <ContentCard
            v-for="series in trendingSeries.slice(0, 4)"
            :key="series.id"
            :item="series"
            contentType="series"
          />
        </div>
      </section>

      <!-- Feature Section -->
      <section class="glass-panel p-8 rounded-2xl my-16">
        <h2 class="text-2xl font-bold text-white mb-8 text-center">
          AI-Powered Film Experience
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div
              class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-900/50 text-primary-400 mb-4"
            >
              <!-- icon SVG -->
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">Smart Recommendations</h3>
            <p class="text-gray-400">
              Our AI learns your preferences to suggest content you'll love.
            </p>
          </div>
          <div class="text-center">
            <div
              class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-accent-900/50 text-accent-400 mb-4"
            >
              <!-- icon SVG -->
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">Personalized Watchlists</h3>
            <p class="text-gray-400">
              Create and manage your own watchlists to track what you want to see.
            </p>
          </div>
          <div class="text-center">
            <div
              class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-secondary-900/50 text-secondary-400 mb-4"
            >
              <!-- icon SVG -->
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">Community Ratings</h3>
            <p class="text-gray-400">
              Rate and review your favorite content and see what others think.
            </p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useContentStore } from '../stores/contentStore'
import { useAuthStore } from '../stores/authStore'
import ContentCard from '../components/ui/ContentCard.vue'

const contentStore = useContentStore()
const authStore = useAuthStore()

const isLoading = ref(true)
const trendingMovies = ref<any[]>([])
const trendingSeries = ref<any[]>([])
const recommendations = ref<any[]>([])

onMounted(async () => {
  try {
    await Promise.all([
      contentStore.fetchTrending(),
      authStore.isAuthenticated
        ? contentStore.fetchRecommendations()
        : Promise.resolve()
    ])
    trendingMovies.value = contentStore.trendingMovies
    trendingSeries.value = contentStore.trendingSeries
    recommendations.value = Array.isArray(contentStore.recommendations)
      ? contentStore.recommendations
      : []
  } catch (e) {
    console.error('Failed to load content', e)
  } finally {
    isLoading.value = false
  }
})

const getContentType = (item: any) => {
  if (!item || typeof item !== 'object') return null
  return 'title' in item ? 'movie' : 'series'
}
</script>

<style scoped>
/* İstersen buraya ekstra stiller ekleyebilirsin */
</style>
