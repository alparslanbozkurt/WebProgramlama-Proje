<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
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
const userComments = ref([])
const isInWatchlist = ref(false)

// Series ID from route params
const seriesId = computed(() => Number(route.params.id))

// Fetch series details on component mount
onMounted(async () => {
  if (seriesId.value) {
    try {
      await contentStore.fetchSeriesDetails(seriesId.value)
      // Fetch user's rating and watchlist status if authenticated
      if (authStore.isAuthenticated) {
        // Mock data for now
        currentRating.value = 4
        isInWatchlist.value = false
        
        // Mock comments data
        userComments.value = [
          {
            id: 1,
            username: 'seriesfan42',
            text: 'This show keeps getting better with each episode. The character development is fantastic!',
            created_at: '2023-11-10T14:23:00Z'
          },
          {
            id: 2,
            username: 'tvcritic',
            text: 'Great production values and compelling storylines. Looking forward to the next season!',
            created_at: '2023-11-09T10:15:00Z'
          }
        ]
      }
    } catch (e) {
      console.error('Failed to load series details', e)
    } finally {
      isLoading.value = false
    }
  }
})

// Get the current series from store
const series = computed(() => contentStore.currentSeries)

// Format first air date
const formattedFirstAirDate = computed(() => {
  if (!series.value?.first_air_date) return ''
  
  const date = new Date(series.value.first_air_date)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
})

// Handle rating change
async function handleRating(rating: number) {
  if (!authStore.isAuthenticated) return
  
  try {
    await contentStore.rateContent(seriesId.value, 'series', rating)
    currentRating.value = rating
  } catch (e) {
    console.error('Failed to rate series', e)
  }
}

// Handle watchlist toggle
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

// Handle new comment
function handleCommentPosted(success: boolean) {
  if (success) {
    // In a real app, we would fetch the updated comments
    // For now, we'll mock adding a new comment
    userComments.value.unshift({
      id: Date.now(),
      username: authStore.user?.username || 'Anonymous',
      text: 'Great series, can\'t wait for the next episode!',
      created_at: new Date().toISOString()
    })
  }
}

// Format comment date
function formatCommentDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>

<template>
  <div>
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>
    
    <!-- Series Details -->
    <div v-else-if="series">
      <!-- Backdrop Header -->
      <div class="relative -mx-4 h-[60vh] min-h-[400px] max-h-[600px] mb-8 overflow-hidden">
        <!-- Backdrop image -->
        <div class="absolute inset-0">
          <img 
            :src="series.backdrop_path || series.poster_path" 
            :alt="series.name" 
            class="w-full h-full object-cover object-center"
          />
          <!-- Overlay gradient -->
          <div class="absolute inset-0 bg-gradient-to-t from-dark-950 via-dark-900/80 to-transparent"></div>
        </div>
        
        <!-- Content overlay -->
        <div class="absolute bottom-0 left-0 right-0 p-6 md:p-8 z-10">
          <div class="container mx-auto flex flex-col md:flex-row items-end">
            <!-- Poster -->
            <div class="hidden md:block w-48 h-72 rounded-lg overflow-hidden shadow-lg">
              <img 
                :src="series.poster_path" 
                :alt="series.name" 
                class="w-full h-full object-cover"
              />
            </div>
            
            <!-- Info -->
            <div class="md:ml-8 md:flex-1">
              <h1 class="text-4xl md:text-5xl font-bold text-white mb-2">{{ series.name }}</h1>
              
              <div class="flex flex-wrap items-center text-sm text-gray-300 mb-4">
                <span>{{ formattedFirstAirDate }}</span>
                <span v-if="series.number_of_seasons" class="mx-2">•</span>
                <span v-if="series.number_of_seasons">{{ series.number_of_seasons }} Season{{ series.number_of_seasons > 1 ? 's' : '' }}</span>
                <span v-if="series.genres && series.genres.length" class="mx-2">•</span>
                <span v-if="series.genres && series.genres.length">{{ series.genres.join(', ') }}</span>
              </div>
              
              <div class="flex items-center mb-4">
                <div class="flex items-center bg-dark-800/80 px-3 py-1 rounded-lg">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-400 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span class="font-medium">{{ (series.vote_average / 2).toFixed(1) }}</span>
                </div>
                
                <div class="ml-4">
                  <button 
                    v-if="authStore.isAuthenticated"
                    @click="toggleWatchlist"
                    class="btn btn-ghost text-sm"
                  >
                    <template v-if="isInWatchlist">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                      In Watchlist
                    </template>
                    <template v-else>
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                      </svg>
                      Add to Watchlist
                    </template>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="container mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Left Content: Overview -->
          <div class="lg:col-span-2">
            <section class="glass-panel p-6 mb-8">
              <h2 class="text-xl font-semibold text-white mb-4">Overview</h2>
              <p class="text-gray-300 leading-relaxed">{{ series.overview }}</p>
            </section>
            
            <!-- User Rating Section -->
            <section class="glass-panel p-6 mb-8">
              <h2 class="text-xl font-semibold text-white mb-4">Your Rating</h2>
              
              <div v-if="!authStore.isAuthenticated" class="text-yellow-400 mb-2">
                Please <router-link to="/login" class="text-accent-400 hover:text-accent-300">log in</router-link> to rate this series.
              </div>
              
              <div v-else class="flex items-center">
                <RatingStars 
                  :initialRating="currentRating" 
                  @update:rating="handleRating" 
                  size="lg"
                />
              </div>
            </section>
            
            <!-- Comments Section -->
            <section class="glass-panel p-6 mb-8">
              <h2 class="text-xl font-semibold text-white mb-4">Comments</h2>
              
              <!-- Comment Form -->
              <CommentBox 
                :contentId="seriesId" 
                contentType="series"
                @comment-posted="handleCommentPosted"
                class="mb-6"
              />
              
              <!-- Comments List -->
              <div v-if="userComments.length === 0" class="text-gray-400 text-center py-4">
                No comments yet. Be the first to comment!
              </div>
              
              <div v-else class="space-y-4">
                <div
                  v-for="comment in userComments"
                  :key="comment.id"
                  class="border-b border-gray-800 pb-4 last:border-b-0 last:pb-0"
                >
                  <div class="flex justify-between items-start mb-2">
                    <div class="flex items-center">
                      <div class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-white mr-3">
                        <span>{{ comment.username.charAt(0).toUpperCase() }}</span>
                      </div>
                      <span class="font-medium text-white">{{ comment.username }}</span>
                    </div>
                    <span class="text-gray-500 text-sm">{{ formatCommentDate(comment.created_at) }}</span>
                  </div>
                  <p class="text-gray-300">{{ comment.text }}</p>
                </div>
              </div>
            </section>
          </div>
          
          <!-- Right Sidebar: Additional Info -->
          <div>
            <!-- Series Poster (Mobile only) -->
            <div class="md:hidden mb-6">
              <img 
                :src="series.poster_path" 
                :alt="series.name" 
                class="w-full rounded-lg shadow-lg"
              />
            </div>
            
            <!-- Series Details -->
            <div class="glass-panel p-6 mb-6">
              <h3 class="text-lg font-semibold text-white mb-4">Series Details</h3>
              
              <div class="space-y-3">
                <div>
                  <span class="text-gray-400 block text-sm">First Air Date:</span>
                  <span class="text-white">{{ formattedFirstAirDate }}</span>
                </div>
                
                <div v-if="series.number_of_seasons">
                  <span class="text-gray-400 block text-sm">Seasons:</span>
                  <span class="text-white">{{ series.number_of_seasons }}</span>
                </div>
                
                <div v-if="series.genres && series.genres.length">
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
              </div>
            </div>
            
            <!-- Recommendations -->
            <div class="glass-panel p-6">
              <h3 class="text-lg font-semibold text-white mb-4">You May Also Like</h3>
              
              <div class="text-gray-400 text-center py-4">
                Recommendations coming soon!
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Error State -->
    <div v-else class="text-center py-16">
      <h2 class="text-2xl font-bold text-white mb-4">Series Not Found</h2>
      <p class="text-gray-400 mb-8">The series you're looking for doesn't exist or has been removed.</p>
      <router-link to="/" class="btn btn-primary">Back to Home</router-link>
    </div>
  </div>
</template>