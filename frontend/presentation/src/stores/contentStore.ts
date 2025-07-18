import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../services/api'

export interface Movie {
  id: number
  title: string
  overview: string
  poster_path: string
  backdrop_path?: string
  release_date: string
  vote_average: number
  genres: string[]
  runtime?: number
  director?: string
  cast?: string[]
  trailerUrl?: string
  similarMovies?: Movie[]
}

export interface Series {
  id: number
  name: string
  overview: string
  poster_path: string
  backdrop_path?: string
  first_air_date: string
  vote_average: number
  genres: string[]
  number_of_seasons: number
  number_of_episodes: number
  episode_run_time: number[]
  cast?: string[]
  videos?: {
    results: {
      key: string
      type: string
    }[]
  }
  similarSeries?: Series[]
  seasons: Season[]
  current_episode?: Episode
}

export interface Season {
  id: number
  season_number: number
  name: string
  episode_count: number
  episodes: Episode[]
}

export interface Episode {
  id: number
  episode_number: number
  name: string
  overview: string
  still_path?: string
  air_date: string
  runtime: number
  watched: boolean
}

export interface WatchProgress {
  contentId: number
  contentType: 'movie' | 'series'
  episodeId?: number
  progress: number
  lastWatched: string
}

export interface CustomList {
  id: number
  name: string
  description: string
  isPrivate: boolean
  items: (Movie | Series)[]
}

// Backend’den dönecek Review objesinin şekli
export interface Review {
  id: number
  user: string          // örn. username
  movie?: number        // Nullable, backend’e göre film ya da dizi için
  tvshow?: number       // Nullable
  rating: number
  comment: string
  created_at: string
}

export const useContentStore = defineStore('content', () => {
  const api = useApi()

  // State
  const trendingMovies = ref<Movie[]>([])
  const trendingSeries = ref<Series[]>([])
  const recommendations = ref<(Movie | Series)[]>([])
  const watchlist = ref<(Movie | Series)[]>([])
  const customLists = ref<CustomList[]>([])
  const currentMovie = ref<Movie | null>(null)
  const currentSeries = ref<Series | null>(null)
  const watchProgress = ref<WatchProgress[]>([])
  const reviews = ref<Review[]>([])
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const genres = ref<string[]>([])

  // Getters
  const allTrending = computed(() => {
    return [...trendingMovies.value, ...trendingSeries.value]
  })

  const nextEpisode = computed(() => {
    if (!currentSeries.value) return null

    for (const season of currentSeries.value.seasons) {
      for (const episode of season.episodes) {
        if (!episode.watched) {
          return episode
        }
      }
    }
    return null
  })

  // -------------------------------
  // Review’ları çekmek: film ya da dizi için
  // -------------------------------
  async function fetchReviews(contentType: 'movie' | 'tvshow', id: number) {
    isLoading.value = true
    error.value = null
    try {
      let res
      if (contentType === 'movie') {
        res = await api.get(`/reviews/?movie=${id}`)
      } else {
        res = await api.get(`/reviews/?tvshow=${id}`)
      }
      reviews.value = res.data
    } catch (e: any) {
      error.value = e.response?.data || e.message
      reviews.value = []
    } finally {
      isLoading.value = false
    }
  }

  // -------------------------------
  // Yeni review eklemek: film ya da dizi için
  // -------------------------------
  async function addReview(
    contentType: 'movie' | 'tvshow',
    id: number,
    rating: number,
    comment: string
  ) {
    try {
      const payload: Record<string, any> = {
        rating,
        comment
      }
      if (contentType === 'movie') {
        payload.movie = id
      } else {
        payload.tvshow = id
      }

      const res = await api.post('/reviews/', payload)
      reviews.value.unshift(res.data)
      return true
    } catch (e: any) {
      error.value = e.response?.data || e.message
      return false
    }
  }

  // -------------------------------
  // Tür listesini çekmek
  // -------------------------------
  async function fetchGenres() {
    try {
      const res = await api.get('/genres/')
      genres.value = res.data.map((g: { id: number; name: string }) => g.name)
    } catch (e: any) {
      console.error('fetchGenres hatası:', e)
      genres.value = []
    }
  }

  // Actions
  async function fetchTrending() {
    isLoading.value = true
    error.value = null
    try {
      const [moviesRes, seriesRes] = await Promise.all([
        api.get('/movies/trending/'),
        api.get('/tvshows/trending/')
      ])
      console.log('>> raw movies:', moviesRes.data)
      trendingMovies.value = moviesRes.data
      trendingSeries.value = seriesRes.data
    } catch (e: any) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMovieDetails(id: number) {
    isLoading.value = true
    error.value = null
    try {
      const res = await api.get(`/movies/${id}/`)
      currentMovie.value = res.data
      isLoading.value = false
      return currentMovie.value
    } catch (e: any) {
      error.value = e.message
      isLoading.value = false
      throw e
    }
  }

  async function fetchSeriesDetails(id: number) {
    isLoading.value = true
    error.value = null
    try {
      const res = await api.get(`/tvshows/${id}/`)
      currentSeries.value = res.data
      isLoading.value = false
      return currentSeries.value
    } catch (e: any) {
      error.value = e.message
      isLoading.value = false
      throw e
    }
  }

  async function fetchWatchlist() {
    isLoading.value = true
    try {
      const mockWatchlist = [
        {
          id: 1,
          title: 'Movie 1',
          overview: 'A great movie',
          poster_path:
            'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
          release_date: new Date().toISOString(),
          vote_average: 4.5,
          genres: ['Action']
        },
        {
          id: 2,
          name: 'Series 1',
          overview: 'A great series',
          poster_path:
            'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
          first_air_date: new Date().toISOString(),
          vote_average: 4.5,
          genres: ['Drama'],
          number_of_seasons: 2,
          seasons: []
        }
      ]

      watchlist.value = mockWatchlist
      isLoading.value = false
    } catch (e: any) {
      error.value = e.message
      watchlist.value = []
      isLoading.value = false
    }
  }

  async function updateWatchProgress(
    contentId: number,
    contentType: 'movie' | 'series',
    progress: number,
    episodeId?: number
  ) {
    try {
      const progressEntry = watchProgress.value.find(
        p =>
          p.contentId === contentId &&
          p.contentType === contentType &&
          (!episodeId || p.episodeId === episodeId)
      )

      if (progressEntry) {
        progressEntry.progress = progress
        progressEntry.lastWatched = new Date().toISOString()
      } else {
        watchProgress.value.push({
          contentId,
          contentType,
          episodeId,
          progress,
          lastWatched: new Date().toISOString()
        })
      }

      if (contentType === 'series' && episodeId && currentSeries.value) {
        currentSeries.value.seasons.forEach(season => {
          season.episodes.forEach(episode => {
            if (episode.id === episodeId) {
              episode.watched = progress >= 0.9
            }
          })
        })
      }

      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function createCustomList(
    name: string,
    description: string,
    isPrivate: boolean
  ) {
    try {
      const newList: CustomList = {
        id: customLists.value.length + 1,
        name,
        description,
        isPrivate,
        items: []
      }

      customLists.value.push(newList)
      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function addToCustomList(
    listId: number,
    contentId: number,
    contentType: 'movie' | 'series'
  ) {
    try {
      const list = customLists.value.find(l => l.id === listId)
      if (list) {
        const content =
          contentType === 'movie'
            ? trendingMovies.value.find(m => m.id === contentId)
            : trendingSeries.value.find(s => s.id === contentId)

        if (content && !list.items.find(item => item.id === contentId)) {
          list.items.push(content)
        }
      }

      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function addToWatchlist(
    contentId: number,
    contentType: 'movie' | 'series'
  ) {
    try {
      const content =
        contentType === 'movie'
          ? trendingMovies.value.find(m => m.id === contentId)
          : trendingSeries.value.find(s => s.id === contentId)

      if (content && !watchlist.value.find(item => item.id === contentId)) {
        watchlist.value.push(content)
      }

      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function removeFromWatchlist(
    contentId: number,
    contentType: 'movie' | 'series'
  ) {
    try {
      watchlist.value = watchlist.value.filter(item => item.id !== contentId)
      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function likeReview(reviewId: number) {
    try {
      const review = reviews.value.find(r => r.id === reviewId)
      if (review) {
        review.rating = review.rating // (şimdilik negative; gerçek like endpoint’i eklenebilir)
      }
      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function addToWatched(
    contentId: number,
    contentType: 'movie' | 'series'
  ) {
    try {
      return await updateWatchProgress(contentId, contentType, 1)
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function removeFromWatched(
    contentId: number,
    contentType: 'movie' | 'series'
  ) {
    try {
      return await updateWatchProgress(contentId, contentType, 0)
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  return {
    trendingMovies,
    trendingSeries,
    recommendations,
    watchlist,
    customLists,
    currentMovie,
    currentSeries,
    watchProgress,
    reviews,
    isLoading,
    error,
    genres,
    fetchGenres,
    allTrending,
    nextEpisode,
    fetchTrending,
    fetchMovieDetails,
    fetchSeriesDetails,
    updateWatchProgress,
    createCustomList,
    addToCustomList,
    addToWatchlist,
    removeFromWatchlist,
    fetchReviews,
    addReview,
    likeReview,
    fetchWatchlist,
    fetchRecommendations: fetchTrending,
    addToWatched,
    removeFromWatched
  }
})
