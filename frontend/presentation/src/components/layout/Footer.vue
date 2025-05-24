<script setup lang="ts">
import { ref } from 'vue'

const year = ref(new Date().getFullYear())
</script>

<template>
  <footer class="bg-dark-900 border-t border-gray-800 py-8">
    <div class="container mx-auto px-4">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="mb-4 md:mb-0">
          <div class="flex items-center">
            <span class="text-2xl font-bold"><span class="text-accent-400">AI</span>Film</span>
          </div>
          <p class="text-gray-400 mt-2 text-sm">Your personal AI-powered film recommendation engine</p>
        </div>
        
        <div class="flex flex-col md:flex-row md:space-x-8">
          <div class="mb-4 md:mb-0">
            <h3 class="text-white font-medium mb-2">Navigation</h3>
            <ul class="space-y-2">
              <li><router-link to="/" class="text-gray-400 hover:text-white transition-colors">Home</router-link></li>
              <li><router-link to="/watchlist" class="text-gray-400 hover:text-white transition-colors">Watchlist</router-link></li>
              <li><router-link to="/profile" class="text-gray-400 hover:text-white transition-colors">Profile</router-link></li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-white font-medium mb-2">Legal</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Terms of Service</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Privacy Policy</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Cookie Policy</a></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="border-t border-gray-800 mt-8 pt-8 text-center">
        <p class="text-gray-500 text-sm">© {{ year }} AIFilm. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>