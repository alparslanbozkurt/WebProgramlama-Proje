<!-- frontend/src/components/ui/CommentBox.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../../stores/authStore'
import { useContentStore } from '../../stores/contentStore'
import { useRouter } from 'vue-router'

/**
 * Props:
 *  - contentId: number   → Hangi film ya da dizi ID’sine yorum yapılıyor
 *  - contentType: 'movie' | 'series'
 */
const props = defineProps<{
  contentId: number
  contentType: 'movie' | 'series'
}>()

const emit = defineEmits<{
  'comment-posted': [success: boolean]
}>()

const authStore = useAuthStore()
const contentStore = useContentStore()
const router = useRouter()

const commentText = ref('')
const rating = ref(0)      // Eğer sadece metin değil yıldız puanı da alacaksanız
const isSubmitting = ref(false)
const error = ref('')

async function submitComment() {
  error.value = ''

  if (!commentText.value.trim()) {
    error.value = 'Comment cannot be empty'
    return
  }

  if (!authStore.isAuthenticated) {
    error.value = 'You must be logged in to post a comment'
    // İstersen, kullanıcıyı login sayfasına yönlendirebilirsin:
    // router.push('/login')
    return
  }

  isSubmitting.value = true

  try {
    // ★ Burada gerçek API çağrısını yapıyoruz:
    const success = await contentStore.addReview(
      props.contentType,    // 'movie' veya 'tvshow' (sizin store’da 'series' yerine 'tvshow' filter ediliyorsa buna göre map edin)
      props.contentId,
      rating.value,         // Eğer rating zorunlu değilse, 0 gönderebilirsiniz
      commentText.value.trim()
    )

    isSubmitting.value = false

    if (success) {
      commentText.value = ''
      rating.value = 0
      emit('comment-posted', true)
    } else {
      error.value = 'Failed to post comment'
      emit('comment-posted', false)
    }
  } catch (e: any) {
    isSubmitting.value = false
    error.value = e.message || 'Failed to post comment'
    emit('comment-posted', false)
  }
}
</script>

<template>
  <div class="glass-panel p-4">
    <h3 class="text-lg font-medium text-white mb-2">Add a Comment</h3>

    <!-- Eğer oturum açık değilse -->
    <div v-if="!authStore.isAuthenticated" class="text-yellow-400 mb-2">
      Please
      <router-link to="/login" class="text-accent-400 hover:text-accent-300">
        log in
      </router-link>
      to post a comment.
    </div>

    <!-- Oturum açıksa formu göster -->
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

      <!-- Eğer rating da almak istiyorsanız bu alanı kullanın -->
      <div class="mb-3 flex items-center space-x-2">
        <label class="text-gray-300">Your Rating:</label>
        <!-- Örnek: basit select ile 1-5 arası puan -->
        <select v-model="rating" :disabled="isSubmitting" class="form-input w-20">
          <option :value="0">0</option>
          <option :value="1">1</option>
          <option :value="2">2</option>
          <option :value="3">3</option>
          <option :value="4">4</option>
          <option :value="5">5</option>
        </select>
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

<script lang="ts">
export default {
  name: 'CommentBox'
}
</script>
