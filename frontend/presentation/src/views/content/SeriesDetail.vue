<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useContentStore, type Series } from '../../stores/contentStore'
import { useAuthStore } from '../../stores/authStore'
import RatingStars from '../../components/ui/RatingStars.vue'
import CommentBox  from '../../components/ui/CommentBox.vue'

const route        = useRoute()
const contentStore = useContentStore()
const authStore    = useAuthStore()

// State
const isLoading     = ref(true)
const currentRating = ref(0)
const isInWatchlist = ref(false)
const hasWatched    = ref(false)
const reviews = computed(() => contentStore.reviews)
const activeTab     = ref<'overview'|'cast'|'reviews'|'similar'>('overview')
const error         = ref<string|null>(null)
const aiTip         = ref('Based on viewer patterns, most people binge-watch this series over a weekend')

// Series ID from route
const seriesId = computed(() => {
  const id = route.params.id
  return id ? Number(id) : null
})

// Series data from store
const series = computed<Series|undefined>(() => contentStore.currentSeries)

// Formatted fields
const formattedFirstAirDate = computed(() => {
  const d = series.value?.first_air_date
  return d
    ? new Date(d).toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' })
    : ''
})

const formattedRuntime = computed(() => {
  const runtimes = series.value?.episode_run_time || []
  if (!runtimes.length) return ''
  // average runtime
  const avg = Math.round(runtimes.reduce((a,b) => a + b, 0) / runtimes.length)
  const h = Math.floor(avg / 60), m = avg % 60
  return `${h}h ${m}m`
})

const seasonsCount  = computed(() => series.value?.number_of_seasons  ?? 0)
const episodesCount = computed(() => series.value?.number_of_episodes ?? 
  // if not available, sum from seasons
  series.value?.seasons?.reduce((sum, s) => sum + s.episode_count, 0) ?? 0
)

// Find trailer video from videos.results array
const trailerVideoId = computed(() => {
  const vids = series.value?.videos?.results
  if (!vids?.length) return null
  try {
    const trailer = vids.find(v => v.type === 'Trailer')
    return trailer?.key ?? null
  } catch {
    return null
  }
})

// Component mount
onMounted(async () => {
  if (!seriesId.value) {
    error.value = 'Invalid series ID'
    isLoading.value = false
    return
  }

  try {
    await contentStore.fetchSeriesDetails(seriesId.value)
    await contentStore.fetchReviews('tvshow', seriesId.value)
    if (authStore.isAuthenticated) {
      currentRating.value = 0
      isInWatchlist.value = false
      hasWatched.value = false
    }
  } catch (e) {
    console.error('Failed to load series details', e)
    error.value = 'Failed to load series details'
  } finally {
    isLoading.value = false
  }
})

// User rating handler
async function handleRating(r: number) {
  if (!authStore.isAuthenticated || !seriesId.value) return
  try {
    await contentStore.addReview(seriesId.value, 'series', r, '')
    currentRating.value = r
  } catch (e) {
    console.error('Failed to submit rating', e)
  }
}

// Watchlist toggle
async function toggleWatchlist() {
  if (!authStore.isAuthenticated || !seriesId.value) return
  try {
    if (isInWatchlist.value) {
      await contentStore.removeFromWatchlist(seriesId.value)
    } else {
      await contentStore.addToWatchlist(seriesId.value, 'series')
    }
    isInWatchlist.value = !isInWatchlist.value
  } catch (e) {
    console.error('Failed to update watchlist', e)
  }
}

// Watched toggle
async function toggleWatched() {
  if (!authStore.isAuthenticated || !seriesId.value) return
  try {
    if (hasWatched.value) {
      await contentStore.removeFromWatched(seriesId.value, 'series')
    } else {
      await contentStore.addToWatched(seriesId.value, 'series')
    }
    hasWatched.value = !hasWatched.value
  } catch (e) {
    console.error('Failed to update watched status', e)
  }
}

// New comment handler
async function handleCommentPosted(success: boolean) {
  if (success && seriesId.value) {
    await contentStore.fetchSeriesDetails(seriesId.value)
  }
}

// Review like handler
async function handleLikeReview(id: number) {
  try {
    await contentStore.likeReview(id)
  } catch (e) {
    console.error('Failed to like review', e)
  }
}

// Date formatter helper
function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', { year:'numeric', month:'short', day:'numeric' })
}
</script>

<template>
  <div>
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center py-16">
      <div class="animate-spin h-12 w-12 border-t-2 border-b-2 border-primary-500 rounded-full"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16">
      <h2 class="text-2xl text-white mb-4">{{ error }}</h2>
      <router-link to="/" class="btn btn-primary">Back to Home</router-link>
    </div>

    <!-- Series detail -->
    <div v-else-if="series" class="pb-12">
      <!-- Backdrop header -->
      <div class="relative h-[60vh] mb-8 overflow-hidden">
         <img
            :src="series.backdrop_path
                ? TMDB_IMG_BASE + series.backdrop_path
                : (series.poster_path ? TMDB_IMG_BASE + series.poster_path : '/fallback-poster.png')"
            :alt="series.name"
            class="w-full h-full object-cover object-center"
          />
        <div class="absolute inset-0 bg-gradient-to-t from-dark-950 via-dark-900/80 to-transparent"></div>
        <div class="absolute bottom-0 left-0 right-0 p-6 container mx-auto flex items-end">
          <!-- Poster (desktop) -->
          <div class="hidden md:block w-48 h-72 shadow-lg overflow-hidden rounded-lg">
             <img
            :src="series.backdrop_path
                ? TMDB_IMG_BASE + series.backdrop_path
                : (series.poster_path ? TMDB_IMG_BASE + series.poster_path : '/fallback-poster.png')"
            :alt="series.name"
            class="w-full h-full object-cover object-center"
          />
          </div>
          <!-- Info -->
          <div class="md:ml-8 flex-1 text-white">
            <h1 class="text-4xl md:text-5xl font-bold mb-2">{{ series.name }}</h1>
            <div class="flex flex-wrap text-gray-300 mb-4 text-sm">
              <span>{{ formattedFirstAirDate }}</span>
              <span v-if="formattedRuntime"  class="mx-2">•</span>
              <span v-if="formattedRuntime">{{ formattedRuntime }}</span>
              <span v-if="seasonsCount"      class="mx-2">•</span>
              <span v-if="seasonsCount">{{ seasonsCount }} seasons</span>
              <span v-if="episodesCount"     class="mx-2">•</span>
              <span v-if="episodesCount">{{ episodesCount }} episodes</span>
            </div>
            <div class="flex items-center space-x-4 mb-6">
              <div class="flex items-center bg-dark-800/80 px-3 py-1 rounded-lg">
                <svg class="h-5 w-5 text-yellow-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927..."/>
                </svg>
                <span>{{ (series.vote_average/2).toFixed(1) }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  v-if="authStore.isAuthenticated"
                  @click="toggleWatchlist"
                  :class="isInWatchlist ? 'btn btn-ghost border-primary-500 text-primary-400' : 'btn btn-ghost'"
                >
                  <svg class="h-5 w-5 mr-1" fill="none" stroke="currentColor">
                    <path d="M12 4v16..."/>
                  </svg>
                  {{ isInWatchlist ? 'In Watchlist' : 'Add to Watchlist' }}
                </button>
                <button
                  v-if="authStore.isAuthenticated"
                  @click="toggleWatched"
                  :class="hasWatched ? 'btn btn-success' : 'btn btn-ghost'"
                >
                  <svg class="h-5 w-5 mr-1" fill="none" stroke="currentColor">
                    <path d="M5 13l4..."/>
                  </svg>
                  {{ hasWatched ? 'Watched' : 'Mark as Watched' }}
                </button>
              </div>
            </div>
            <p class="text-gray-300 line-clamp-3">{{ series.overview }}</p>

            <!-- AI Tip -->
            <div v-if="aiTip" class="mt-4 bg-primary-900/50 backdrop-blur-sm rounded-lg p-4 border border-primary-700/50">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center flex-shrink-0 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <p class="text-primary-200 italic">{{ aiTip }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sekmeler -->
      <div class="container mx-auto">
        <div class="flex border-b border-gray-800 mb-8 overflow-x-auto">
          <button
            v-for="tab in ['overview','cast','reviews','similar']"
            :key="tab"
            @click="activeTab = tab"
            class="px-6 py-3 text-sm font-medium border-b-2 transition-colors"
            :class="activeTab === tab
              ? 'text-primary-400 border-primary-400'
              : 'text-gray-400 border-transparent hover:text-gray-300'"
          >
            {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
          </button>
        </div>
        <div class="grid lg:grid-cols-3 gap-8">
          <!-- Ana içerik -->
          <div class="lg:col-span-2 space-y-8">
            <!-- Overview -->
            <section v-if="activeTab === 'overview'" class="space-y-6">
              <div v-if="trailerVideoId" class="glass-panel p-6">
                <h2 class="text-xl font-semibold text-white mb-4">Trailer</h2>
                <div class="relative pb-[56.25%]">
                  <iframe
                    :src="`https://www.youtube.com/embed/${trailerVideoId}`"
                    class="absolute inset-0 w-full h-full rounded-lg"
                    frameborder="0"
                    allowfullscreen
                  />
                </div>
              </div>
              <div class="glass-panel p-6">
                <h2 class="text-xl font-semibold text-white mb-4">Synopsis</h2>
                <p class="text-gray-300">{{ series.overview }}</p>
              </div>
            </section>

            <!-- Cast -->
            <section v-if="activeTab === 'cast'" class="glass-panel p-6">
              <h2 class="text-xl font-semibold text-white mb-6">Cast & Crew</h2>
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
                <div v-for="actor in series.cast" :key="actor" class="text-center">
                  <div class="w-full aspect-square bg-dark-700 rounded-lg mb-3 overflow-hidden">
                    <img src="https://via.placeholder.com/150" class="w-full h-full object-cover"/>
                  </div>
                  <h3 class="text-white">{{ actor }}</h3>
                  <p class="text-gray-400 text-sm">Character</p>
                </div>
              </div>
            </section>

            <!-- Reviews -->
            <div v-if="activeTab === 'reviews'" class="space-y-6">
              <!-- User Rating kısmı (aynen kalsın) -->
              <section class="glass-panel p-6">
                <h2 class="text-xl font-semibold text-white mb-4">Your Rating</h2>
                <div v-if="!authStore.isAuthenticated" class="text-yellow-400 mb-2">
                  Please
                  <router-link to="/login" class="text-accent-400 hover:text-accent-300"
                    >log in</router-link
                  >
                  to rate this movie.
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

                <!-- Comment Form (sadece girişli kullanıcı görebilecek) -->
                <CommentBox
                  v-if="authStore.isAuthenticated"
                  :contentId="seriesId"
                  contentType="series"
                  @comment-posted="handleCommentPosted"
                  class="mb-6"
                />
                <div v-else class="text-gray-400 text-center py-4">
                  Please log in to post a review.
                </div>

                <!-- Yorum Listesi: Eğer hiç review yoksa “No reviews” mesajı -->
                <div v-if="reviews.length === 0" class="text-gray-400 text-center py-4">
                  No reviews yet. Be the first to review!
                </div>
                <div v-else class="space-y-6">
                  <div
                    v-for="review in reviews"
                    :key="review.id"
                    class="border-b border-gray-800 pb-6 last:border-b-0 last:pb-0"
                  >
                    <div class="flex justify-between items-start mb-2">
                      <div class="flex items-center">
                        <div
                          class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-white mr-3"
                        >
                          <span>{{ review.user.charAt(0).toUpperCase() }}</span>
                        </div>
                        <div>
                          <span class="font-medium text-white block">{{ review.user }}</span>
                          <RatingStars :initialRating="review.rating" readOnly size="sm" />
                        </div>
                      </div>
                      <span class="text-gray-500 text-sm">
                        {{ formatDate(review.created_at) }}
                      </span>
                    </div>
                    <p class="text-gray-300 mt-2">{{ review.comment }}</p>
                    <div class="flex items-center mt-4">
                      <button
                        @click="handleLikeReview(review.id)"
                        class="flex items-center text-gray-400 hover:text-primary-400 transition-colors"
                      >
                        👍
                        <span class="ml-1">{{ review.rating }} </span>
                      </button>
                    </div>
                  </div>
                </div>
              </section>
            </div>

            <!-- Similar -->
            <section v-if="activeTab === 'similar'" class="glass-panel p-6">
              <h2 class="text-xl font-semibold text-white mb-6">Similar Series</h2>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-6">
                <div
                  v-for="s in series.similarSeries"
                  :key="s.id"
                  class="relative group rounded-lg overflow-hidden"
                >
                  <img
                    :src="s.poster_path"
                    class="w-full aspect-[2/3] object-cover transition-transform group-hover:scale-110"
                  />
                  <div class="absolute inset-0 bg-gradient-to-t from-dark-950 to-transparent opacity-0 group-hover:opacity-100"></div>
                  <router-link :to="`/series/${s.id}`" class="absolute inset-0 z-10"></router-link>
                  <div class="absolute bottom-0 p-4 text-white">
                    <h3 class="font-medium">{{ s.name }}</h3>
                    <div class="flex items-center text-sm text-gray-300">
                      <span>{{ new Date(s.first_air_date).getFullYear() }}</span>
                      <span class="mx-1">•</span>
                      <span>{{ (s.vote_average/2).toFixed(1) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- Sidebar -->
          <aside class="space-y-6">
            <div class="glass-panel p-6">
              <h3 class="text-lg font-semibold text-white mb-4">Details</h3>
              <div class="space-y-4 text-gray-300 text-sm">
                <div>
                  <span class="block">First Air Date</span>
                  <span class="text-white">{{ formattedFirstAirDate }}</span>
                </div>
                <div v-if="formattedRuntime">
                  <span class="block">Episode Runtime Avg</span>
                  <span class="text-white">{{ formattedRuntime }}</span>
                </div>
                <div>
                  <span class="block">Seasons</span>
                  <span class="text-white">{{ seasonsCount }}</span>
                </div>
                <div>
                  <span class="block">Episodes</span>
                  <span class="text-white">{{ episodesCount }}</span>
                </div>
                <div>
                  <span class="block">User Score</span>
                  <span class="text-white">{{ (series.vote_average/2).toFixed(1) }}/5</span>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>

    <!-- Not Found State -->
    <div v-else class="text-center py-16">
      <h2 class="text-2xl text-white mb-4">Series Not Found</h2>
      <router-link to="/" class="btn btn-primary">Back to Home</router-link>
    </div>
  </div>
</template>