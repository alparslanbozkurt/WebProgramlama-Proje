import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

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

export const useMovieStore = defineStore('movies', () => {
  // State
  const movies = ref<Movie[]>([])
  const watchlist = ref<Movie[]>([])
  const currentMovie = ref<Movie | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Mock data generation
  function generateMockMovies(): Movie[] {
    return Array.from({ length: 10 }, (_, i) => ({
      id: i + 1,
      title: `Movie ${i + 1}`,
      overview: 'A fascinating story that will keep you on the edge of your seat.',
      poster_path: 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
      release_date: new Date().toISOString(),
      vote_average: 4.5,
      genres: ['Action', 'Drama'],
      runtime: 120,
      director: 'John Director',
      cast: ['Actor 1', 'Actor 2', 'Actor 3'],
      trailerUrl: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    }))
  }

  // Actions
  async function fetchMovies() {
    isLoading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      movies.value = generateMockMovies()
    } catch (e: any) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMovieDetails(id: number) {
    isLoading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      const movie = movies.value.find(m => m.id === id) || generateMockMovies()[0]
      currentMovie.value = {
        ...movie,
        similarMovies: generateMockMovies().slice(0, 4)
      }
    } catch (e: any) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  async function addToWatchlist(movie: Movie) {
    if (!watchlist.value.find(m => m.id === movie.id)) {
      watchlist.value.push(movie)
      // Store in localStorage
      localStorage.setItem('watchlist', JSON.stringify(watchlist.value))
    }
  }

  async function removeFromWatchlist(movieId: number) {
    watchlist.value = watchlist.value.filter(m => m.id !== movieId)
    // Update localStorage
    localStorage.setItem('watchlist', JSON.stringify(watchlist.value))
  }

  // Initialize watchlist from localStorage
  function initializeWatchlist() {
    const stored = localStorage.getItem('watchlist')
    if (stored) {
      watchlist.value = JSON.parse(stored)
    }
  }

  return {
    movies,
    watchlist,
    currentMovie,
    isLoading,
    error,
    fetchMovies,
    fetchMovieDetails,
    addToWatchlist,
    removeFromWatchlist,
    initializeWatchlist
  }
})