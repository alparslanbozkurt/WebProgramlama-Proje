<script setup lang="ts">
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
)
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/authStore'
import { useContentStore } from '../../stores/contentStore'
import { format } from 'date-fns'
import { toast } from 'vue3-toastify'
import { useRouter } from 'vue-router'
import 'vue3-toastify/dist/index.css'
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';
import { storeToRefs } from 'pinia'

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp('(^|;\\s*)(' + name + ')=([^;]*)'));
  return match ? decodeURIComponent(match[3]) : null;
}


const authStore = useAuthStore()
const contentStore = useContentStore()
const imagePreview = ref<string | null>(null)
const csrfToken = ref(getCookie('csrftoken'));

// State
const isLoading = ref(true)
const activeTab = ref('profile')
const { user, isAuthenticated } = storeToRefs(authStore)
const router = useRouter()
const watchHistory = ref([])
const favoriteGenres = ref(['Action', 'Drama', 'Sci-Fi'])
const notificationPreferences = ref({
  emailNotifications: true,
  pushNotifications: false,
  newContentAlerts: true,
  watchlistReminders: true
})
// Profile picture upload
const showImageCropper = ref(false)
const imageFile = ref(null)
const croppedImage = ref(null)

// Account settings
const accountForm = ref({
  username: user.value?.username || '',
  email: user.value?.email || '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Watch history chart data
const watchHistoryData = ref({
  labels: [],
  datasets: [{
    label: 'Watch Time (hours)',
    data: [],
    borderColor: '#4F46E5',
    tension: 0.4
  }]
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#9CA3AF' }
    },
    x: {
      grid: { color: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#9CA3AF' }
    }
  },
  plugins: {
    legend: {
      labels: { color: '#9CA3AF' }
    }
  }
}

// Methods
function handleImageUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] ?? null
  if (file) {
    if (imagePreview.value) {
      URL.revokeObjectURL(imagePreview.value)
    }
    imageFile.value = file
    imagePreview.value = URL.createObjectURL(file)
    showImageCropper.value = true
  }
}

async function saveCroppedImage() {
  try {
    const blob = await (await fetch(croppedImage.value)).blob()
    const formData = new FormData()
    formData.append('profile_picture', blob, 'profile.jpg')

    const res = await fetch('/api/accounts/upload-profile-picture/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrfToken.value || ''
      },
      body: formData
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Upload failed')

    // Başarılıysa Vue içindeki user görselini de güncelle
    user.value.profile_image = URL.createObjectURL(blob)
    showImageCropper.value = false
    toast.success('Profile picture updated successfully!')
  } catch (error) {
    toast.error(error.message || 'Failed to update profile picture')
  }
}


async function updateProfile() {
  try {
    // In a real app, make API call to update profile
    user.value = {
      ...user.value,
      username: accountForm.value.username,
      email: accountForm.value.email
    }
    toast.success('Profile updated successfully!')
  } catch (error) {
    toast.error('Failed to update profile')
  }
}

async function updatePassword() {
  try {
    if (accountForm.value.newPassword !== accountForm.value.confirmPassword) {
      throw new Error('Passwords do not match')
    }
    // In a real app, make API call to update password
    toast.success('Password updated successfully!')
    accountForm.value.currentPassword = ''
    accountForm.value.newPassword = ''
    accountForm.value.confirmPassword = ''
  } catch (error) {
    toast.error(error.message || 'Failed to update password')
  }
}

async function updateNotifications() {
  try {
    // In a real app, make API call to update notification preferences
    toast.success('Notification preferences updated!')
  } catch (error) {
    toast.error('Failed to update notification preferences')
  }
}

async function toggleGenre(genre: string) {
  const isAdding = !favoriteGenres.value.includes(genre)
  try {
    const res = await fetch('/api/accounts/favorite-genres/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken.value || ''
      },
      body: JSON.stringify({
        genre,
        action: isAdding ? 'add' : 'remove'
      })
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Failed to update favorite genres')

    // local state güncelle
    if (isAdding) {
      favoriteGenres.value.push(genre)
    } else {
      favoriteGenres.value = favoriteGenres.value.filter(g => g !== genre)
    }

  } catch (error) {
    console.error(error)
    toast.error('Could not update favorite genres')
  }
}


const allGenres = ref<string[]>([])

onMounted(async () => {
  // Eğer kullanıcı yok ama token varsa, kullanıcı bilgilerini çek
  if (!authStore.user && authStore.accessToken) {
    await authStore.fetchUser()
  }

  // CSRF kontrolü
  csrfToken.value = getCookie('csrftoken')
  if (!csrfToken.value) {
    console.warn("CSRF token bulunamadı.")
  }

  // Auth değilse yönlendir
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  // Watch history
  watchHistory.value = Array.from({ length: 7 }, (_, i) => ({
    date: format(new Date(Date.now() - i * 24 * 60 * 60 * 1000), 'MMM dd'),
    hours: Math.floor(Math.random() * 5)
  })).reverse()
  watchHistoryData.value.labels = watchHistory.value.map(item => item.date)
  watchHistoryData.value.datasets[0].data = watchHistory.value.map(item => item.hours)

  // 🔥 Genre'leri çek
  try {
    const res = await fetch('/api/genres/', {
      headers: { 'Content-Type': 'application/json' }
    })
    const data = await res.json()
    allGenres.value = data.map((genre: any) => genre.name) // sadece isimlerini al
  } catch (err) {
    toast.error('Could not fetch genres from server')
    console.error(err)
  }

  // Kullanıcının favori türlerini çek
try {
  const res = await fetch('/api/accounts/favorite-genres/', {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const data = await res.json()
  favoriteGenres.value = data.genres  // örnek response: { "genres": ["Action", "Comedy"] }
} catch (err) {
  console.error('Could not fetch favorite genres:', err)
}

  isLoading.value = false
})


</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-white mb-6">My Profile</h1>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
    </div>

    <!-- Profile Content -->
    <div v-else-if="user" class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Sidebar -->
      <div class="lg:col-span-1">
        <div class="glass-panel p-6 rounded-lg">
          <!-- Profile Picture -->
          <div class="text-center mb-6">
            <div class="relative inline-block">
              <div class="w-32 h-32 rounded-full overflow-hidden bg-gray-700 mb-4">
                <img 
                  v-if="user.profile_image" 
                  :src="user.profile_image" 
                  :alt="user.username"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center text-4xl text-white">
                  {{ user.username.charAt(0).toUpperCase() }}
                </div>
              </div>
              <label class="absolute bottom-0 right-0 bg-primary-600 rounded-full p-2 cursor-pointer hover:bg-primary-700 transition-colors">
                <input type="file" class="hidden" accept="image/*" @change="handleImageUpload" />
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </label>
            </div>
            <h2 class="text-xl font-semibold text-white">{{ user.username }}</h2>
            <p class="text-gray-400">Member since {{ new Date(user.created_at).toLocaleDateString() }}</p>
          </div>

          <!-- Navigation -->
          <nav class="space-y-2">
            <button 
              v-for="tab in ['profile', 'history', 'preferences', 'security']" 
              :key="tab"
              @click="activeTab = tab"
              class="w-full text-left px-4 py-2 rounded-lg transition-colors"
              :class="activeTab === tab ? 'bg-primary-600 text-white' : 'text-gray-300 hover:bg-dark-700'"
            >
              {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Main Content -->
      <div class="lg:col-span-3 space-y-6">
        <!-- Profile Tab -->
        <div v-if="activeTab === 'profile'" class="glass-panel p-6 rounded-lg">
          <h3 class="text-xl font-semibold text-white mb-6">Account Information</h3>
          <form @submit.prevent="updateProfile" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Username</label>
              <input 
                type="text" 
                v-model="accountForm.username"
                class="form-input w-full"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Email</label>
              <input 
                type="email" 
                v-model="accountForm.email"
                class="form-input w-full"
              />
            </div>
            <button type="submit" class="btn btn-primary">Save Changes</button>
          </form>
        </div>

        <!-- Watch History Tab -->
        <div v-if="activeTab === 'history'" class="space-y-6">
          <div class="glass-panel p-6 rounded-lg">
            <h3 class="text-xl font-semibold text-white mb-6">Watch History</h3>
            <div class="h-64">
              <Line 
                :data="watchHistoryData"
                :options="chartOptions"
              />
            </div>
          </div>

          <div class="glass-panel p-6 rounded-lg">
            <h3 class="text-xl font-semibold text-white mb-6">Recently Watched</h3>
            <div class="space-y-4">
              <div v-for="(item, index) in watchHistory" :key="index" class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-12 h-12 rounded bg-dark-700"></div>
                  <div class="ml-4">
                    <p class="text-white">Movie Title {{ index + 1 }}</p>
                    <p class="text-sm text-gray-400">{{ item.date }}</p>
                  </div>
                </div>
                <span class="text-gray-400">{{ item.hours }}h</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Preferences Tab -->
        <div v-if="activeTab === 'preferences'" class="space-y-6">
          <!-- Notification Preferences -->
          <div class="glass-panel p-6 rounded-lg">
            <h3 class="text-xl font-semibold text-white mb-6">Notification Preferences</h3>
            <div class="space-y-4">
              <label class="flex items-center">
                <input 
                  type="checkbox" 
                  v-model="notificationPreferences.emailNotifications"
                  class="form-checkbox rounded text-primary-600"
                />
                <span class="ml-2 text-gray-300">Email Notifications</span>
              </label>
              <label class="flex items-center">
                <input 
                  type="checkbox" 
                  v-model="notificationPreferences.pushNotifications"
                  class="form-checkbox rounded text-primary-600"
                />
                <span class="ml-2 text-gray-300">Push Notifications</span>
              </label>
              <label class="flex items-center">
                <input 
                  type="checkbox" 
                  v-model="notificationPreferences.newContentAlerts"
                  class="form-checkbox rounded text-primary-600"
                />
                <span class="ml-2 text-gray-300">New Content Alerts</span>
              </label>
              <label class="flex items-center">
                <input 
                  type="checkbox" 
                  v-model="notificationPreferences.watchlistReminders"
                  class="form-checkbox rounded text-primary-600"
                />
                <span class="ml-2 text-gray-300">Watchlist Reminders</span>
              </label>
              <button @click="updateNotifications" class="btn btn-primary mt-4">Save Preferences</button>
            </div>
          </div>

          <!-- Favorite Genres -->
          <div class="glass-panel p-6 rounded-lg">
            <h3 class="text-xl font-semibold text-white mb-6">Favorite Genres</h3>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="genre in allGenres"
                :key="genre"
                @click="toggleGenre(genre)"
                :class="[
                  'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                  favoriteGenres?.value?.includes(genre)
                    ? 'bg-primary-600 text-white'
                    : 'bg-dark-700 text-gray-300 hover:bg-dark-600'
                ]"
              >
                {{ genre }}
              </button>
            </div>
          </div>

        </div>

        <!-- Security Tab -->
        <div v-if="activeTab === 'security'" class="glass-panel p-6 rounded-lg">
          <h3 class="text-xl font-semibold text-white mb-6">Change Password</h3>
          <form @submit.prevent="updatePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Current Password</label>
              <input 
                type="password" 
                v-model="accountForm.currentPassword"
                class="form-input w-full"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">New Password</label>
              <input 
                type="password" 
                v-model="accountForm.newPassword"
                class="form-input w-full"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Confirm New Password</label>
              <input 
                type="password" 
                v-model="accountForm.confirmPassword"
                class="form-input w-full"
              />
            </div>
            <button type="submit" class="btn btn-primary">Update Password</button>
          </form>
        </div>
      </div>
    </div>

    <!-- Image Cropper Modal -->
    <div v-if="showImageCropper" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="glass-panel p-6 rounded-lg w-full max-w-2xl">
        <h3 class="text-xl font-semibold text-white mb-4">Crop Profile Picture</h3>
        <Cropper
          v-if="imagePreview"
          :src="imagePreview"
          @change="croppedImage = $event.canvas.toDataURL()"
          class="h-96"
        />

        <div class="flex justify-end space-x-4 mt-4">
          <button @click="showImageCropper = false" class="btn btn-ghost">Cancel</button>
          <button @click="saveCroppedImage" class="btn btn-primary">Save</button>
        </div>
      </div>
    </div>

    <!-- Not Authenticated -->
    <div v-else class="text-center py-16">
      <h2 class="text-2xl font-bold text-white mb-4">Please log in to view your profile</h2>
      <router-link to="/login" class="btn btn-primary">Log In</router-link>
    </div>
  </div>
</template>