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

export interface Review {
  id: number
  userId: number
  username: string
  contentId: number
  contentType: 'movie' | 'series'
  rating: number
  comment: string
  createdAt: string
  likes: number
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

      // Actions
      async function fetchTrending() {
      isLoading.value = true;
      error.value = null;
      try {
        // Aynı anda hem film hem dizi isteği yap
        const [moviesRes, seriesRes] = await Promise.all([
          api.get('/movies/trending/'),
          api.get('/tvshows/trending/')
        ]);
        console.log('>> raw movies:', moviesRes.data)
        // Dönen verileri state’e ata
        trendingMovies.value = moviesRes.data;
        trendingSeries.value = seriesRes.data;
      } catch (e: any) {
        error.value = e.message;
      } finally {
        isLoading.value = false;
      }
    }

  async function fetchMovieDetails(id: number) {
    isLoading.value = true
    error.value = null
    
    try {
      // For demo purposes, create mock movie data
      currentMovie.value = {
        id,
        title: `Movie ${id}`,
        overview: 'A fascinating story that will keep you on the edge of your seat. This movie explores themes of love, adventure, and redemption in a way that has never been seen before. With stunning visuals and a compelling narrative, it\'s a must-watch for any film enthusiast.',
        poster_path: 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
        backdrop_path: 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
        release_date: new Date().toISOString(),
        vote_average: 4.5,
        genres: ['Action', 'Drama', 'Adventure'],
        runtime: 142,
        director: 'John Director',
        cast: ['Actor 1', 'Actor 2', 'Actor 3'],
        trailerUrl: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        similarMovies: Array.from({ length: 4 }, (_, i) => ({
          id: i + 100,
          title: `Similar Movie ${i + 1}`,
          overview: 'Another great movie you might enjoy.',
          poster_path: 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
          release_date: new Date().toISOString(),
          vote_average: 4.3,
          genres: ['Action', 'Drama']
        }))
      }
      
      // Fetch mock reviews
      reviews.value = Array.from({ length: 5 }, (_, i) => ({
        id: i + 1,
        userId: i + 1,
        username: `user${i + 1}`,
        contentId: id,
        contentType: 'movie',
        rating: 4 + Math.random(),
        comment: 'This movie was amazing! The performances were outstanding and the story kept me engaged throughout.',
        createdAt: new Date().toISOString(),
        likes: Math.floor(Math.random() * 50)
      }))
      
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
    try {
      // For demo purposes, create mock series data
      currentSeries.value = {
        id,
        name: `Series ${id}`,
        overview: 'An epic series that will captivate you from start to finish.',
        poster_path: 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
        backdrop_path: 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
        first_air_date: new Date().toISOString(),
        vote_average: 4.5,
        genres: ['Drama', 'Thriller'],
        number_of_seasons: 3,
        seasons: Array.from({ length: 3 }, (_, i) => ({
          id: i + 1,
          season_number: i + 1,
          name: `Season ${i + 1}`,
          episode_count: 10,
          episodes: Array.from({ length: 10 }, (_, j) => ({
            id: j + 1,
            episode_number: j + 1,
            name: `Episode ${j + 1}`,
            overview: 'An exciting episode full of twists and turns.',
            air_date: new Date().toISOString(),
            runtime: 45,
            watched: false
          }))
        }))
      }
      
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
      // For demo purposes, create mock watchlist data
      const mockWatchlist = [
        {
          id: 1,
          title: 'Movie 1',
          overview: 'A great movie',
          poster_path: 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
          release_date: new Date().toISOString(),
          vote_average: 4.5,
          genres: ['Action']
        },
        {
          id: 2,
          name: 'Series 1',
          overview: 'A great series',
          poster_path: 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
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

  async function updateWatchProgress(contentId: number, contentType: 'movie' | 'series', progress: number, episodeId?: number) {
    try {
      // Update local state
      const progressEntry = watchProgress.value.find(p => 
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
      
      // Update episode watched status for series
      if (contentType === 'series' && episodeId && currentSeries.value) {
        currentSeries.value.seasons.forEach(season => {
          season.episodes.forEach(episode => {
            if (episode.id === episodeId) {
              episode.watched = progress >= 0.9 // Mark as watched if progress is >= 90%
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
  
  async function createCustomList(name: string, description: string, isPrivate: boolean) {
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
  
  async function addToCustomList(listId: number, contentId: number, contentType: 'movie' | 'series') {
    try {
      const list = customLists.value.find(l => l.id === listId)
      if (list) {
        const content = contentType === 'movie' 
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

  async function addToWatchlist(contentId: number, contentType: 'movie' | 'series') {
    try {
      // For demo purposes, just add to local state
      const content = contentType === 'movie'
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

  async function removeFromWatchlist(contentId: number, contentType: 'movie' | 'series') {
    try {
      watchlist.value = watchlist.value.filter(item => item.id !== contentId)
      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function addReview(contentId: number, contentType: 'movie' | 'series', rating: number, comment: string) {
    try {
      const newReview: Review = {
        id: reviews.value.length + 1,
        userId: 1, // Demo user ID
        username: 'demo_user',
        contentId,
        contentType,
        rating,
        comment,
        createdAt: new Date().toISOString(),
        likes: 0
      }
      
      reviews.value.unshift(newReview)
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
        review.likes++
      }
      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function addToWatched(contentId: number, contentType: 'movie' | 'series') {
    try {
      // For demo purposes, just update watch progress to 100%
      return await updateWatchProgress(contentId, contentType, 1)
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function removeFromWatched(contentId: number, contentType: 'movie' | 'series') {
    try {
      // For demo purposes, just update watch progress to 0%
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
    addReview,
    likeReview,
    fetchWatchlist,
    fetchRecommendations: fetchTrending, // For demo purposes, use same data
    addToWatched,
    removeFromWatched
  }
})