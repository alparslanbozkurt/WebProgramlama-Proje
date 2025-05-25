<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../../stores/authStore'

const props = defineProps<{
  contentId: number
  contentType: 'movie' | 'series'
}>()

const emit = defineEmits<{
  'comment-posted': [success: boolean]
}>()

const authStore = useAuthStore()
const commentText = ref('')
const isSubmitting = ref(false)
const error = ref('')

async function submitComment() {
  if (!commentText.value.trim()) {
    error.value = 'Comment cannot be empty'
    return
  }
  
  if (!authStore.isAuthenticated) {
    error.value = 'You must be logged in to post a comment'
    return
  }
  
  isSubmitting.value = true
  error.value = ''
  
  try {
    // API çağrısı buraya gelecek simülasyonu bu şekilde 
    await new Promise(resolve => setTimeout(resolve, 500))
    commentText.value = ''
    isSubmitting.value = false
    emit('comment-posted', true)
  } catch (e: any) {
    error.value = e.message || 'Failed to post comment'
    isSubmitting.value = false
    emit('comment-posted', false)
  }
}
</script>

<template>
  <div class="glass-panel p-4">
    <h3 class="text-lg font-medium text-white mb-2">Add a Comment</h3>
    <div v-if="!authStore.isAuthenticated" class="text-yellow-400 mb-2">
      Please <router-link to="/login" class="text-accent-400 hover:text-accent-300">log in</router-link> to post a comment.
    </div>
    <form v-else @submit.prevent="submitComment">
      <div class="mb-3">
        <textarea
          v-model="commentText"
          rows="3"
          placeholder="Write your comment here..."
          class="form-input w-full"
          :disabled="isSubmitting"
        ></textarea>
        <p v-if="error" class="text-error-500 text-sm mt-1">{{ error }}</p>
      </div>
      <div class="flex justify-end">
        <button 
          type="submit" 
          class="btn btn-primary"
          :disabled="isSubmitting"
        >
          <span v-if="isSubmitting">Posting...</span>
          <span v-else>Post Comment</span>
        </button>
      </div>
    </form>
  </div>
</template>