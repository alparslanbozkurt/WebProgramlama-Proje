<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../../stores/authStore'
import { useContentStore } from '../../stores/contentStore'
import { marked } from 'marked'

interface ChatMessage {
  id: number
  content: string
  isUser: boolean
  timestamp: string
}

const authStore = useAuthStore()
const contentStore = useContentStore()

const messages = ref<ChatMessage[]>([])
const newMessage = ref('')
const isLoading = ref(false)
const chatOpen = ref(false)

const addMessage = (content: string, isUser: boolean) => {
  messages.value.push({
    id: Date.now(),
    content,
    isUser,
    timestamp: new Date().toISOString()
  })
}

const handleSubmit = async () => {
  if (!newMessage.value.trim()) return

  const userMessage = newMessage.value
  addMessage(userMessage, true)
  newMessage.value = ''
  isLoading.value = true

  try {
    //AI endpointleri burda
    await new Promise(resolve => setTimeout(resolve, 1000))
    const response = await generateResponse(userMessage)
    addMessage(response, false)
  } catch (error) {
    console.error('Failed to get response:', error)
    addMessage('Sorry, I encountered an error. Please try again.', false)
  } finally {
    isLoading.value = false
  }
}

const generateResponse = async (message: string): Promise<string> => {
  // Buraya gerçek AI integrasyonu ile değiştirin
  const responses = [
    "Based on your interests, I recommend watching 'Inception'. It's a mind-bending sci-fi thriller that you might enjoy.",
    "Have you considered watching 'The Shawshank Redemption'? It's a classic that consistently ranks among the best movies of all time.",
    "Given your recent viewing history, you might enjoy 'Interstellar'. It combines sci-fi elements with emotional depth.",
    "I think you'd love 'Pulp Fiction'. It's known for its unique narrative structure and memorable characters."
  ]
  return responses[Math.floor(Math.random() * responses.length)]
}

const toggleChat = () => {
  chatOpen.value = !chatOpen.value
}


const formatTime = (timestamp: string) => {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}


const renderMarkdown = (content: string) => {
  return marked(content)
}
</script>

<template>
  <div class="fixed bottom-4 right-4 z-50">
   
    <button 
      @click="toggleChat"
      class="btn btn-primary rounded-full p-4 shadow-lg hover:shadow-xl transition-all duration-300"
    >
      <svg 
        v-if="!chatOpen"
        xmlns="http://www.w3.org/2000/svg" 
        class="h-6 w-6" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
        />
      </svg>
      <svg 
        v-else
        xmlns="http://www.w3.org/2000/svg" 
        class="h-6 w-6" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M6 18L18 6M6 6l12 12"
        />
      </svg>
    </button>

    
    <div 
      v-if="chatOpen"
      class="absolute bottom-20 right-0 w-96 glass-panel rounded-lg shadow-xl overflow-hidden"
    >
      
      <div class="bg-dark-800 p-4 border-b border-gray-700">
        <h3 class="text-lg font-semibold text-white">Movie Assistant</h3>
        <p class="text-sm text-gray-400">Ask me about movies and get personalized recommendations</p>
      </div>

      
      <div class="h-96 overflow-y-auto p-4 space-y-4">
        <div 
          v-for="message in messages" 
          :key="message.id"
          :class="[
            'flex',
            message.isUser ? 'justify-end' : 'justify-start'
          ]"
        >
          <div 
            :class="[
              'max-w-[80%] rounded-lg p-3',
              message.isUser 
                ? 'bg-primary-600 text-white' 
                : 'bg-dark-700 text-gray-200'
            ]"
          >
            <div 
              class="prose prose-sm prose-invert"
              v-html="renderMarkdown(message.content)"
            ></div>
            <div 
              :class="[
                'text-xs mt-1',
                message.isUser ? 'text-primary-200' : 'text-gray-400'
              ]"
            >
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Loading indikatörü-->
        <div v-if="isLoading" class="flex justify-start">
          <div class="bg-dark-700 rounded-lg p-3">
            <div class="flex space-x-2">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
          </div>
        </div>
      </div>

      
      <div class="p-4 border-t border-gray-700">
        <form @submit.prevent="handleSubmit" class="flex space-x-2">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Ask about movies..."
            class="form-input flex-1"
            :disabled="isLoading"
          />
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="isLoading || !newMessage.trim()"
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>