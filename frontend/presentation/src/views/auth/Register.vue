<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const errorMessage = ref('')

const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Form validation
function validateForm() {
  if (!formData.username || !formData.email || !formData.password || !formData.confirmPassword) {
    errorMessage.value = 'All fields are required'
    return false
  }
  
  if (formData.password !== formData.confirmPassword) {
    errorMessage.value = 'Passwords do not match'
    return false
  }
  
  // Basic email validation
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailPattern.test(formData.email)) {
    errorMessage.value = 'Please enter a valid email address'
    return false
  }
  
  // Password strength validation
  if (formData.password.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters long'
    return false
  }
  
  return true
}

// Handle registration submission
async function handleSubmit() {
  if (!validateForm()) return
  
  loading.value = true
  errorMessage.value = ''
  
  const success = await authStore.register(formData.username, formData.email, formData.password)
  
  loading.value = false
  
  if (success) {
    router.push('/')
  } else {
    errorMessage.value = authStore.error || 'Registration failed'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-dark-950 relative overflow-hidden p-4">
    <!-- Background effect -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute inset-0 bg-[url('https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')] bg-cover bg-center opacity-10"></div>
      <div class="absolute inset-0 bg-gradient-radial from-accent-900/10 to-dark-950"></div>
    </div>
    
    <!-- Registration form -->
    <div class="glass-panel max-w-md w-full p-8 relative z-10">
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-white flex items-center justify-center">
          <span class="text-accent-400 mr-1">AI</span>Film
        </h1>
        <p class="text-gray-300 mt-2">Create your account</p>
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
            placeholder="Choose a username"
          />
        </div>
        
        <div class="mb-4">
          <label for="email" class="form-label">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="formData.email" 
            class="form-input w-full"
            :disabled="loading"
            placeholder="Enter your email"
          />
        </div>
        
        <div class="mb-4">
          <label for="password" class="form-label">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password" 
            class="form-input w-full"
            :disabled="loading"
            placeholder="Create a password"
          />
          <p class="text-gray-500 text-xs mt-1">Must be at least 8 characters long</p>
        </div>
        
        <div class="mb-6">
          <label for="confirmPassword" class="form-label">Confirm Password</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="formData.confirmPassword" 
            class="form-input w-full"
            :disabled="loading"
            placeholder="Confirm your password"
          />
        </div>
        
        <div v-if="errorMessage" class="mb-4 p-3 bg-error-900/50 border border-error-700 text-error-300 rounded-lg text-sm">
          {{ errorMessage }}
        </div>
        
        <button 
          type="submit" 
          class="btn btn-accent w-full"
          :disabled="loading"
        >
          <span v-if="loading">Creating account...</span>
          <span v-else>Create Account</span>
        </button>
      </form>
      
      <div class="mt-6 text-center text-sm">
        <p class="text-gray-400">
          Already have an account? 
          <router-link to="/login" class="text-primary-400 hover:text-primary-300">
            Sign in
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>