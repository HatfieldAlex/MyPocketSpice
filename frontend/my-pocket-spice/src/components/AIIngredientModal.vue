<template>
  <Transition name="modal">
    <div v-if="isOpen" class="modal-overlay" @click.self="close">
      <div class="modal-container">
        <div class="modal-header">
          <h2 class="modal-title">
            <span class="ai-icon">✨</span>
            AI Recipe Match
            <span class="beta-tag">BETA</span>
          </h2>
          <button class="close-button" @click="close" aria-label="Close">
            ×
          </button>
        </div>
        
        <div class="modal-content">
          <p class="modal-description">
            Not sure what to cook? Enter your ingredients and we'll recommend the best match!
          </p>
          
          <div class="input-wrapper">
            <Input
              v-model="ingredients"
              placeholder="e.g., chicken, tomatoes, pasta..."
              @keyup.enter="handleSubmit"
              :disabled="loading"
            />
          </div>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </div>
        
        <div class="modal-footer">
          <Button variant="secondary" @click="close" :disabled="loading">
            Cancel
          </Button>
          <Button variant="accent" @click="handleSubmit" :disabled="loading || !ingredients.trim()">
            <span v-if="loading">Finding Recipe...</span>
            <span v-else>Find Recipe</span>
          </Button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Input from './ui/Input.vue'
import Button from './ui/Button.vue'

interface Props {
  isOpen: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'submit', ingredients: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const ingredients = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

const close = () => {
  if (!loading.value) {
    ingredients.value = ''
    error.value = null
    emit('close')
  }
}

const handleSubmit = () => {
  if (ingredients.value.trim() && !loading.value) {
    loading.value = true
    error.value = null
    emit('submit', ingredients.value.trim())
  }
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    ingredients.value = ''
    error.value = null
    loading.value = false
  }
})

defineExpose({
  setLoading: (value: boolean) => { loading.value = value },
  setError: (err: string | null) => { error.value = err },
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(10, 10, 10, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(10, 10, 10, 0.1), 0 10px 10px -5px rgba(10, 10, 10, 0.04);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e8e8e8;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #0a0a0a;
  margin: 0;
}

.ai-icon {
  font-size: 1.75rem;
}

.beta-tag {
  background: linear-gradient(135deg, #fed1f6 0%, #fdb8f0 100%);
  color: #0a0a0a;
  font-size: 0.625rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-left: 0.5rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 2rem;
  color: #4a4a4a;
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  transition: all 200ms;
}

.close-button:hover {
  background-color: #f5f5f5;
  color: #0a0a0a;
}

.modal-content {
  padding: 1.5rem;
}

.modal-description {
  color: #4a4a4a;
  margin: 0 0 1.5rem 0;
  line-height: 1.6;
}

.input-wrapper {
  margin-bottom: 1rem;
}

.error-message {
  color: #ff4d4f;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background-color: #fff5f5;
  border-radius: 0.5rem;
  border-left: 3px solid #ff4d4f;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #e8e8e8;
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 200ms ease;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 200ms ease, opacity 200ms ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
  opacity: 0;
}

@media (max-width: 640px) {
  .modal-container {
    max-width: 100%;
  }
  
  .modal-title {
    font-size: 1.25rem;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
  }
  
  .modal-footer button {
    width: 100%;
  }
}
</style>

