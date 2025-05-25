<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const loading = ref(false)
const errorMessage = ref('')

const formData = reactive({
  username: '',
  password: ''
})

// Handle login submission
async function handleSubmit() {
  if (!formData.username || !formData.password) {
    errorMessage.value = 'Username and password are required'
    return
  }
  
  loading.value = true
  errorMessage.value = ''
  
  const success = await authStore.login(formData.username, formData.password)
  
  loading.value = false
  
  if (success) {
    // Navigate to the page the user was trying to access,
    // or to the home page by default
    const redirectTo = route.query.redirect as string || '/'
    router.push(redirectTo)
  } else {
    errorMessage.value = authStore.error || 'Invalid login credentials'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-dark-950 relative overflow-hidden p-4">
    <!-- Background effect -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute inset-0 bg-[url('https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')] bg-cover bg-center opacity-10"></div>
      <div class="absolute inset-0 bg-gradient-radial from-primary-900/10 to-dark-950"></div>
    </div>
    
    <!-- Login form -->
    <div class="glass-panel max-w-md w-full p-8 relative z-10">
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-white flex items-center justify-center">
          <span class="text-accent-400 mr-1">AI</span>Film
        </h1>
        <p class="text-gray-300 mt-2">Sign in to your account</p>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label for="username" class="form-label">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="formData.username" 
            class="form-input w-full"
            :disabled="loading"
            placeholder="Enter your username"
          />
        </div>
        
        <div class="mb-6">
          <label for="password" class="form-label">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password" 
            class="form-input w-full"
            :disabled="loading"
            placeholder="Enter your password"
          />
        </div>
        
        <div v-if="errorMessage" class="mb-4 p-3 bg-error-900/50 border border-error-700 text-error-300 rounded-lg text-sm">
          {{ errorMessage }}
        </div>
        
        <button 
          type="submit" 
          class="btn btn-primary w-full"
          :disabled="loading"
        >
          <span v-if="loading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
      </form>
      
      <div class="mt-6 text-center text-sm">
        <p class="text-gray-400">
          Don't have an account? 
          <router-link to="/register" class="text-accent-400 hover:text-accent-300">
            Create one
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>