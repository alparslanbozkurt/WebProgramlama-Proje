<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps<{
  initialRating?: number
  readOnly?: boolean
  size?: 'sm' | 'md' | 'lg'
}>()

const emit = defineEmits<{
  'update:rating': [rating: number]
}>()

const rating = ref(props.initialRating || 0)
const tempRating = ref(0)
const hovering = ref(false)

const maxStars = 5


watch(() => props.initialRating, (newValue) => {
  if (newValue !== undefined) {
    rating.value = newValue
  }
})

const starSize = computed(() => {
  switch (props.size) {
    case 'sm': return 'h-4 w-4'
    case 'lg': return 'h-8 w-8'
    default: return 'h-6 w-6'
  }
})

const displayRating = computed(() => {
  return hovering.value ? tempRating.value : rating.value
})

function hoverStar(index: number) {
  if (props.readOnly) return
  
  hovering.value = true
  tempRating.value = index
}

function resetHover() {
  if (props.readOnly) return
  
  hovering.value = false
  tempRating.value = 0
}

function setRating(index: number) {
  if (props.readOnly) return
  
  rating.value = index
  emit('update:rating', index)
}
</script>

<template>
  <div class="rating" @mouseleave="resetHover">
    <template v-for="i in maxStars" :key="i">
      <button 
        type="button" 
        @click="setRating(i)" 
        @mouseover="hoverStar(i)" 
        :class="[
          'rating-star',
          starSize,
          { 
            'active': i <= displayRating,
            'cursor-default': props.readOnly
          }
        ]"
        :disabled="props.readOnly"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.007 5.404.433c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.433 2.082-5.006z" clip-rule="evenodd" />
        </svg>
      </button>
    </template>
    <span v-if="displayRating > 0" class="ml-2 text-sm text-gray-300">
      {{ displayRating }}/{{ maxStars }}
    </span>
  </div>
</template>