<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

const isAdmin = computed(() => {
  return authStore.user?.role === 'Admin' || authStore.user?.role === 'Editor'
})

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

async function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="fixed top-0 left-0 right-0 bg-dark-900/80 backdrop-blur-md border-b border-gray-800 z-50">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <div class="flex-shrink-0">
          <router-link to="/" class="flex items-center text-2xl font-bold text-white">
            <span class="text-accent-400 mr-1">AI</span>Film
          </router-link>
        </div>
        <nav class="hidden md:flex space-x-4">
          <router-link to="/" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300" active-class="bg-dark-700 text-white">
            Home
          </router-link>
          <router-link v-if="authStore.isAuthenticated" to="/watchlist" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300" active-class="bg-dark-700 text-white">
            My Watchlist
          </router-link>
          <router-link v-if="isAdmin" to="/admin" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300" active-class="bg-dark-700 text-white">
            Admin
          </router-link>
        </nav>
        
        
        <div class="hidden md:flex items-center">
          <template v-if="authStore.isAuthenticated">
            <router-link to="/profile" class="mr-4 flex items-center text-gray-300 hover:text-white transition-colors duration-300">
              <div class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-white">
                <span v-if="!authStore.user?.profile_image">{{ authStore.user?.username.charAt(0).toUpperCase() }}</span>
                <img v-else :src="authStore.user?.profile_image" class="w-8 h-8 rounded-full" :alt="authStore.user?.username">
              </div>
              <span class="ml-2">{{ authStore.user?.username }}</span>
            </router-link>
            <button @click="logout" class="btn btn-ghost">
              Logout
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="mr-4 btn btn-ghost">
              Login
            </router-link>
            <router-link to="/register" class="btn btn-primary">
              Register
            </router-link>
          </template>
        </div>
        
       
        <div class="md:hidden flex items-center">
          <button 
            @click="toggleMobileMenu" 
            class="text-gray-300 hover:text-white focus:outline-none"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path 
                v-if="!mobileMenuOpen" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path 
                v-else 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    
    <div 
      v-if="mobileMenuOpen" 
      class="md:hidden glass-panel m-2 rounded-xl shadow-lg"
    >
      <div class="p-2">
        <router-link 
          to="/" 
          @click="closeMobileMenu"
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300"
          active-class="bg-dark-700 text-white"
        >
          Home
        </router-link>
        <router-link 
          v-if="authStore.isAuthenticated" 
          to="/watchlist" 
          @click="closeMobileMenu"
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300"
          active-class="bg-dark-700 text-white"
        >
          My Watchlist
        </router-link>
        <router-link 
          v-if="authStore.isAuthenticated" 
          to="/profile" 
          @click="closeMobileMenu"
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300"
          active-class="bg-dark-700 text-white"
        >
          My Profile
        </router-link>
        <router-link 
          v-if="isAdmin" 
          to="/admin" 
          @click="closeMobileMenu"
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300"
          active-class="bg-dark-700 text-white"
        >
          Admin Dashboard
        </router-link>
        
        <div class="border-t border-gray-800 my-2 pt-2">
          <template v-if="authStore.isAuthenticated">
            <button 
              @click="logout(); closeMobileMenu()" 
              class="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300"
            >
              Logout
            </button>
          </template>
          <template v-else>
            <router-link 
              to="/login" 
              @click="closeMobileMenu"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-dark-700 transition-colors duration-300"
            >
              Login
            </router-link>
            <router-link 
              to="/register" 
              @click="closeMobileMenu"
              class="block px-3 py-2 rounded-md text-base font-medium bg-primary-600 text-white mt-2 text-center"
            >
              Register
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>