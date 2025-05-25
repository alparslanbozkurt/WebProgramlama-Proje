<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goBack() {
  router.back()
}
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 px-4 text-center">
    <h1 class="text-5xl md:text-7xl font-bold text-white mb-2">404</h1>
    <h2 class="text-2xl md:text-3xl font-bold text-white mb-6">Page Not Found</h2>
    
    <p class="text-gray-300 max-w-md mb-8">
      The page you're looking for doesn't exist or has been moved.
    </p>
    
    <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
      <button @click="goBack" class="btn btn-ghost">
        Go Back
      </button>
      <router-link to="/" class="btn btn-primary">
        Return Home
      </router-link>
    </div>
  </div>
</template>