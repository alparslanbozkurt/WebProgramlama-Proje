<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'
import Navbar from './components/layout/Navbar.vue'
import Footer from './components/layout/Footer.vue'
import ChatBot from './components/chat/ChatBot.vue'

const router = useRouter()
const authStore = useAuthStore()

// Initialize auth from localStorage if available
onMounted(() => {
  authStore.initializeAuth()
})

// Determine if current route is a fullscreen page (login/register)
const isFullscreenPage = computed(() => {
  return router.currentRoute.value.meta.fullscreen
})
</script>

<template>
  <div class="min-h-screen flex flex-col bg-dark-900">
    <!-- Show navbar on all pages except fullscreen pages -->
    <Navbar v-if="!isFullscreenPage" />
    
    <!-- Main content -->
    <main :class="isFullscreenPage ? 'flex-1' : 'flex-1 container mx-auto p-4 mt-16'">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <!-- Show footer on all pages except fullscreen pages -->
    <Footer v-if="!isFullscreenPage" />

    <!-- ChatBot component -->
    <ChatBot v-if="!isFullscreenPage" />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>