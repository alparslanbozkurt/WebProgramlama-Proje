<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useContentStore } from '../../stores/contentStore'
import { useAuthStore } from '../../stores/authStore'

import RatingStars from '../../components/ui/RatingStars.vue'
import CommentBox from '../../components/ui/CommentBox.vue'

const route = useRoute()
const contentStore = useContentStore()
const authStore = useAuthStore()

// State
const isLoading = ref(true)
const currentRating = ref(0)
const isInWatchlist = ref(false)
const hasWatched = ref(false) // Dizi bazında "izlendi" durumu
const activeTab = ref<'overview' | 'cast' | 'reviews' | 'similar'>('overview')

// Series ID from route params
const seriesId = computed(() => Number(route.params.id))

// Görseller için temel URL (env üzerinden veya fallback)
const TMDB_IMG_BASE = import.meta.env.VITE_TMDB_IMG_BASE || 'https://image.tmdb.org/t/p/original'

// Series bilgisini store’dan al
const series = computed(() => contentStore.currentSeries)

// Formatlı tarih
const formattedFirstAirDate = computed(() => {
  if (!series.value?.first_air_date) return ''
  return new Date(series.value.first_air_date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
})

// Eğer dizinin trailerUrl’si varsa YouTube video ID’sini al
const trailerVideoId = computed<string | null>(() => {
  const urlOrKey = series.value?.trailerUrl
  if (!urlOrKey) return null
  try {
    const url = new URL(urlOrKey)
    return url.searchParams.get('v')
  } catch {
    // Eğer yalnızca key geliyorsa
    return urlOrKey
  }
})

// Sayfa yüklendiğinde veya ID değiştiğinde detayları çek
async function loadSeriesDetails(id: number) {
  isLoading.value = true
  try {
    await contentStore.fetchSeriesDetails(id)

    if (authStore.isAuthenticated) {
      currentRating.value = await contentStore.fetchUserRating(id, 'series')
      isInWatchlist.value = await contentStore.checkInWatchlist(id, 'series')
      hasWatched.value = await contentStore.checkHasWatched(id, 'series')
    }
  } catch (e) {
    console.error('Failed to load series details', e)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (seriesId.value) {
    loadSeriesDetails(seriesId.value)
  }
})

watch(
  () => route.params.id,
  (newVal, oldVal) => {
    if (newVal !== oldVal) {
      activeTab.value = 'overview'
      loadSeriesDetails(Number(newVal))
    }
  }
)

// Rating verme
async function handleRating(rating: number) {
  if (!authStore.isAuthenticated) return
  try {
    await contentStore.rateContent(seriesId.value, 'series', rating)
    currentRating.value = rating
  } catch (e) {
    console.error('Failed to rate series', e)
  }
}

// Watchlist ekle/kaldır
async function toggleWatchlist() {
  if (!authStore.isAuthenticated) return
  try {
    if (isInWatchlist.value) {
      await contentStore.removeFromWatchlist(seriesId.value, 'series')
      isInWatchlist.value = false
    } else {
      await contentStore.addToWatchlist(seriesId.value, 'series')
      isInWatchlist.value = true
    }
  } catch (e) {
    console.error('Failed to update watchlist', e)
  }
}

// İzlendi durumunu ekle/kaldır
async function toggleWatched() {
  if (!authStore.isAuthenticated) return
  try {
    if (hasWatched.value) {
      await contentStore.removeFromWatched(seriesId.value, 'series')
      hasWatched.value = false
    } else {
      await contentStore.addToWatched(seriesId.value, 'series')
      hasWatched.value = true
    }
  } catch (e) {
    console.error('Failed to update watched status', e)
  }
}

// Yeni yorum gönderildiğinde dizi detaylarını yenile
async function handleCommentPosted(success: boolean) {
  if (success) {
    await contentStore.fetchSeriesDetails(seriesId.value)
  }
}

// Yorum tarihini formatla
function formatDate(dateString: string) {
  const d = new Date(dateString)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

// İncelemeye (review) like atma
async function handleLikeReview(reviewId: number) {
  await contentStore.likeReview(reviewId)
}
</script>

<template>
  <div>
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <!-- Series Details -->
    <div v-else-if="series" class="pb-12">
      <!-- Backdrop Header -->
      <div class="relative -mx-4 h-[60vh] min-h-[400px] max-h-[600px] mb-8 overflow-hidden">
        <!-- Backdrop image -->
        <div class="absolute inset-0">
          <img
            :src="series.backdrop_path
              ? TMDB_IMG_BASE + series.backdrop_path
              : series.poster_path
              ? TMDB_IMG_BASE + series.poster_path
              : '/fallback-poster.png'"
            :alt="series.name"
            class="w-full h-full object-cover object-center"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-dark-950 via-dark-900/80 to-transparent"></div>
        </div>

        <!-- Content overlay -->
        <div class="absolute bottom-0 left-0 right-0 p-6 md:p-8 z-10">
          <div class="container mx-auto flex flex-col md:flex-row items-end">
            <!-- Poster -->
            <div class="hidden md:block w-48 h-72 rounded-lg overflow-hidden shadow-lg">
              <img
                :src="series.poster_path
                  ? TMDB_IMG_BASE + series.poster_path
                  : '/fallback-poster.png'"
                :alt="series.name"
                class="w-full h-full object-cover object-center"
              />
            </div>

            <!-- Info -->
            <div class="md:ml-8 md:flex-1">
              <h1 class="text-4xl md:text-5xl font-bold text-white mb-2">{{ series.name }}</h1>

              <div class="flex flex-wrap items-center text-sm text-gray-300 mb-4">
                <span>{{ formattedFirstAirDate }}</span>
                <span v-if="series.number_of_seasons" class="mx-2">•</span>
                <span v-if="series.number_of_seasons">
                  {{ series.number_of_seasons }}
                  Season{{ series.number_of_seasons > 1 ? 's' : '' }}
                </span>
                <span v-if="series.genres?.length" class="mx-2">•</span>
                <span v-if="series.genres?.length">{{ series.genres.join(', ') }}</span>
              </div>

              <div class="flex items-center space-x-4 mb-4">
                <!-- Rating (küçük yıldız ikonu + sayı) -->
                <div class="flex items-center bg-dark-800/80 px-3 py-1 rounded-lg">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 text-yellow-400 mr-1"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371
                         1.24.588 1.81l-2.8 2.034a1 1 0 00-.364
                         1.118l1.07 3.292c.3.921-.755
                         1.688-1.54 1.118l-2.8-2.034a1 1
                         0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1
                         1 0 00-.364-1.118L2.98
                         8.72c-.783-.57-.38-1.81.588-1.81h3.461a1
                         1 0 00.951-.69l1.07-3.292z"
                    />
                  </svg>
                  <span class="font-medium">{{ (series.vote_average / 2).toFixed(1) }}</span>
                </div>

                <!-- Actions: Watchlist, Watched -->
                <div class="flex items-center space-x-4 mb-6">
                  <button
                    v-if="authStore.isAuthenticated"
                    @click="toggleWatchlist"
                    class="btn btn-ghost"
                    :class="isInWatchlist ? 'border-primary-500 text-primary-400' : ''"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 mr-2"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    {{ isInWatchlist ? 'In Watchlist' : 'Add to Watchlist' }}
                  </button>

                  <button
                    v-if="authStore.isAuthenticated"
                    @click="toggleWatched"
                    class="btn btn-ghost"
                    :class="hasWatched ? 'btn-success' : ''"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 mr-2"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                    {{ hasWatched ? 'Watched' : 'Mark as Watched' }}
                  </button>
                </div>
              </div>

              <p class="text-gray-300 text-lg leading-relaxed line-clamp-3">{{ series.overview }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="container mx-auto">
        <!-- Navigation Tabs -->
        <div class="flex border-b border-gray-800 mb-8 overflow-x-auto">
          <button
            v-for="tab in ['overview', 'cast', 'reviews', 'similar']"
            :key="tab"
            @click="activeTab = tab"
            class="px-6 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors"
            :class="
              activeTab === tab
                ? 'text-primary-400 border-primary-400'
                : 'text-gray-400 border-transparent hover:text-gray-300'
            "
          >
            {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Left Column -->
          <div class="lg:col-span-2">
            <!-- Overview Tab -->
            <div v-if="activeTab === 'overview'" class="space-y-8">
              <!-- Trailer Section -->
              <section v-if="trailerVideoId" class="glass-panel p-6">
                <h2 class="text-xl font-semibold text-white mb-4">Trailer</h2>
                <div class="relative pb-[56.25%]">
                  <iframe
                    :src="`https://www.youtube.com/embed/${trailerVideoId}`"
                    class="absolute top-0 left-0 w-full h-full rounded-lg"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                  ></iframe>
                </div>
              </section>

              <!-- Synopsis -->
              <section class="glass-panel p-6">
                <h2 class="text-xl font-semibold text-white mb-4">Synopsis</h2>
                <p class="text-gray-300 leading-relaxed">{{ series.overview }}</p>
              </section>

              <!-- Cast & Crew -->
              <section class="glass-panel p-6">
                <h2 class="text-xl font-semibold text-white mb-4">Cast & Crew</h2>
                <div class="space-y-4">
                  <div v-if="series.director">
                    <h3 class="text-gray-400 text-sm">Creator</h3>
                    <p class="text-white">{{ series.director }}</p>
                  </div>
                  <div>
                    <h3 class="text-gray-400 text-sm">Cast</h3>
                    <div class="flex flex-wrap gap-2 mt-2">
                      <span
                        v-for="actor in series.cast"
                        :key="actor"
                        class="px-3 py-1 bg-dark-700 rounded-full text-sm text-gray-300"
                      >
                        {{ actor }}
                      </span>
                    </div>
                  </div>
                </div>
              </section>
            </div>

            <!-- Cast Tab -->
            <div v-if="activeTab === 'cast'" class="glass-panel p-6">
              <h2 class="text-xl font-semibold text-white mb-6">Cast & Crew</h2>
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
                <div
                  v-for="actor in series.cast"
                  :key="actor"
                  class="glass-panel p-4 rounded-lg text-center"
                >
                  <div class="w-full aspect-square bg-dark-700 rounded-lg mb-3 overflow-hidden">
                    <img
                      src="https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg"
                      :alt="actor"
                      class="w-full h-full object-cover"
                    />
                  </div>
                  <h3 class="text-white font-medium mb-1">{{ actor }}</h3>
                  <p class="text-sm text-gray-400">Character</p>
                </div>
              </div>
            </div>

            <!-- Reviews Tab -->
            <div v-if="activeTab === 'reviews'" class="space-y-6">
              <!-- User Rating -->
              <section class="glass-panel p-6">
                <h2 class="text-xl font-semibold text-white mb-4">Your Rating</h2>
                <div v-if="!authStore.isAuthenticated" class="text-yellow-400 mb-2">
                  Please
                  <router-link to="/login" class="text-accent-400 hover:text-accent-300">
                    log in
                  </router-link>
                  to rate this series.
                </div>
                <div v-else class="flex items-center">
                  <RatingStars
                    :initialRating="currentRating"
                    @update:rating="handleRating"
                    size="lg"
                  />
                </div>
              </section>

              <!-- Comments -->
              <section class="glass-panel p-6">
                <h2 class="text-xl font-semibold text-white mb-4">Reviews</h2>

                <!-- Comment Form -->
                <CommentBox
                  :contentId="seriesId"
                  contentType="series"
                  @comment-posted="handleCommentPosted"
                  class="mb-6"
                />

                <!-- Reviews List -->
                <div v-if="contentStore.reviews.length === 0" class="text-gray-400 text-center py-4">
                  No reviews yet. Be the first to review!
                </div>

                <div v-else class="space-y-6">
                  <div
                    v-for="review in contentStore.reviews"
                    :key="review.id"
                    class="border-b border-gray-800 pb-6 last:border-b-0 last:pb-0"
                  >
                    <div class="flex justify-between items-start mb-2">
                      <div class="flex items-center">
                        <div class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-white mr-3">
                          <span>{{ review.username.charAt(0).toUpperCase() }}</span>
                        </div>
                        <div>
                          <span class="font-medium text-white block">{{ review.username }}</span>
                          <RatingStars :initialRating="review.rating" readOnly size="sm" />
                        </div>
                      </div>
                      <span class="text-gray-500 text-sm">{{ formatDate(review.createdAt) }}</span>
                    </div>
                    <p class="text-gray-300 mt-2">{{ review.comment }}</p>
                    <div class="flex items-center mt-4">
                      <button
                        @click="handleLikeReview(review.id)"
                        class="flex items-center text-gray-400 hover:text-primary-400 transition-colors"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          class="h-5 w-5 mr-1"
                          viewBox="0 0 20 20"
                          fill="currentColor"
                        >
                          <path
                            d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6
                              10.333v5.43a2
                              2 0 001.106 1.79l.05.025A4
                              4 0 008.943 18h5.416a2 2 0
                              001.962-1.608l1.2-6A2 2 0
                              0015.56 8H12V4a2 2 0 00-2-2
                              1 1 0 00-1 1v.667a4 4 0
                              01-.8 2.4L6.8 7.933a4 4 0
                              00-.8 2.4z"
                          />
                        </svg>
                        <span>{{ review.likes }}</span>
                      </button>
                    </div>
                  </div>
                </div>
              </section>
            </div>

            <!-- Similar Series Tab -->
            <div v-if="activeTab === 'similar'" class="glass-panel p-6">
              <h2 class="text-xl font-semibold text-white mb-6">Similar Series</h2>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-6">
                <div
                  v-for="sim in series.similarShows"
                  :key="sim.id"
                  class="group relative overflow-hidden rounded-lg"
                >
                  <img
                    :src="sim.poster_path ? TMDB_IMG_BASE + sim.poster_path : '/fallback-poster.png'"
                    :alt="sim.name"
                    class="w-full aspect-[2/3] object-cover transition-transform duration-300 group-hover:scale-110"
                  />
                  <div class="absolute inset-0 bg-gradient-to-t from-dark-950 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <div class="absolute bottom-0 left-0 right-0 p-4">
                      <h3 class="text-white font-medium">{{ sim.name }}</h3>
                      <div class="flex items-center text-sm text-gray-300 mt-1">
                        <span>{{ new Date(sim.first_air_date).getFullYear() }}</span>
                        <span class="mx-2">•</span>
                        <span class="flex items-center">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-400 mr-1" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                          {{ (sim.vote_average / 2).toFixed(1) }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <router-link
                    :to="`/series/${sim.id}`"
                    class="absolute inset-0 z-10"
                  ></router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Series Poster (Mobile only) -->
            <div class="md:hidden mb-6">
              <img
                :src="series.poster_path ? TMDB_IMG_BASE + series.poster_path : '/fallback-poster.png'"
                :alt="series.name"
                class="w-full rounded-lg shadow-lg"
              />
            </div>

            <!-- Series Details Box -->
            <div class="glass-panel p-6">
              <h3 class="text-lg font-semibold text-white mb-4">Series Details</h3>
              <div class="space-y-4">
                <div>
                  <span class="text-gray-400 block text-sm">First Air Date:</span>
                  <span class="text-white">{{ formattedFirstAirDate }}</span>
                </div>

                <div v-if="series.number_of_seasons">
                  <span class="text-gray-400 block text-sm">Seasons:</span>
                  <span class="text-white">{{ series.number_of_seasons }}</span>
                </div>

                <div v-if="series.episode_run_time?.length">
                  <span class="text-gray-400 block text-sm">Episode Runtime:</span>
                  <span class="text-white">{{ series.episode_run_time[0] }} min</span>
                </div>

                <div v-if="series.genres?.length">
                  <span class="text-gray-400 block text-sm">Genres:</span>
                  <div class="flex flex-wrap gap-2 mt-1">
                    <span
                      v-for="genre in series.genres"
                      :key="genre"
                      class="px-2 py-1 text-xs rounded-md bg-dark-700 text-gray-300"
                    >
                      {{ genre }}
                    </span>
                  </div>
                </div>

                <div>
                  <span class="text-gray-400 block text-sm">User Score:</span>
                  <div class="flex items-center">
                    <div class="text-yellow-400 mr-1">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    </div>
                    <span class="text-white">{{ (series.vote_average / 2).toFixed(1) }}/5</span>
                  </div>
                </div>

                <div v-if="series.networks?.length">
                  <span class="text-gray-400 block text-sm">Network:</span>
                  <span class="text-white">{{ series.networks[0] }}</span>
                </div>
              </div>
            </div>

            <!-- External Links -->
            <div class="glass-panel p-6">
              <h3 class="text-lg font-semibold text-white mb-4">External Links</h3>
              <div class="space-y-2">
                <a
                  v-if="series.homepage"
                  :href="series.homepage"
                  target="_blank"
                  class="flex items-center text-gray-300 hover:text-white transition-colors"
                >
                  <span class="mr-2">Official Website</span>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
                <a
                  v-if="series.imdb_id"
                  :href="`https://www.imdb.com/title/${series.imdb_id}`"
                  target="_blank"
                  class="flex items-center text-gray-300 hover:text-white transition-colors"
                >
                  <span class="mr-2">IMDb Page</span>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="text-center py-16">
      <h2 class="text-2xl font-bold text-white mb-4">Series Not Found</h2>
      <p class="text-gray-400 mb-8">
        The series you're looking for doesn't exist or has been removed.
      </p>
      <router-link to="/" class="btn btn-primary">Back to Home</router-link>
    </div>
  </div>
</template>

<style scoped>
/* Gerekirse eklenen stil kuralları buraya */
</style>
