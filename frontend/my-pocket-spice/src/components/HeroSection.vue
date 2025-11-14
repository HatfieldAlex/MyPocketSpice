<template>
  <section class="hero-section">
    <div class="hero-background"></div>
    <div class="hero-overlay"></div>
    <Container>
      <div class="hero-content">
        <h1 class="hero-title">Discover Delicious Recipes</h1>
        <p class="hero-subtitle">Explore our curated collection of mouth-watering dishes from around the world.</p>
        
        <div class="search-wrapper">
          <Input
            v-model="searchQuery"
            placeholder="Search recipes..."
            @update:model-value="handleSearch"
          />
          <Button variant="accent" size="lg" @click="handleSearch">
            Search
          </Button>
        </div>
        
        <div class="ai-suggestion-wrapper">
          <Button variant="primary" size="md" class="ai-button" @click="openAIModal">
            <span class="ai-icon">✨</span>
            <span>Not sure what to cook? Enter your ingredients and we'll recommend the best match!</span>
            <span class="beta-tag">BETA</span>
          </Button>
        </div>
      </div>
    </Container>
    
    <AIIngredientModal
      :is-open="isModalOpen"
      @close="closeModal"
      @submit="handleAISubmit"
      ref="modalRef"
    />
    
    <Transition name="loading-overlay">
      <div v-if="isAILoading" class="loading-overlay">
        <AILoadingState />
      </div>
    </Transition>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Container from './ui/Container.vue'
import Input from './ui/Input.vue'
import Button from './ui/Button.vue'
import AIIngredientModal from './AIIngredientModal.vue'
import AILoadingState from './AILoadingState.vue'
import { apiClient } from '@/api/client'

const router = useRouter()
const searchQuery = ref('')
const isModalOpen = ref(false)
const isAILoading = ref(false)
const modalRef = ref<InstanceType<typeof AIIngredientModal> | null>(null)

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/recipes',
      query: { q: searchQuery.value.trim() },
    })
  } else {
    router.push('/recipes')
  }
}

const openAIModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const handleAISubmit = async (ingredients: string) => {
  if (!ingredients.trim()) return
  
  isAILoading.value = true
  modalRef.value?.setLoading(true)
  
  try {
    const response = await apiClient.aiMatchRecipes(ingredients)
    
    // Navigate to recipe detail page with AI explanation
    router.push({
      path: `/recipes/${response.recipe.id}`,
      query: {
        ai: 'true',
        justification: encodeURIComponent(response.justification)
      }
    })
    
    // Close modal and reset state
    isModalOpen.value = false
    isAILoading.value = false
  } catch (error) {
    modalRef.value?.setError(error instanceof Error ? error.message : 'Failed to find recipe match')
    modalRef.value?.setLoading(false)
    isAILoading.value = false
  }
}
</script>

<style scoped>
.hero-section {
  position: relative;
  padding: 6rem 0;
  overflow: hidden;
  min-height: 500px;
  display: flex;
  align-items: center;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('@/assets/hero-background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  filter: blur(1px);
  transform: scale(1.02);
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.9) 0%,
    rgba(255, 255, 255, 0.8) 50%,
    rgba(255, 255, 255, 0.9) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  color: #0a0a0a;
  margin: 0 0 1.5rem 0;
  line-height: 1.2;
  text-align: center;
}

.hero-subtitle {
  font-size: 1.25rem;
  font-weight: 400;
  color: #4a4a4a;
  margin: 0 0 3rem 0;
  line-height: 1.6;
  text-align: center;
}

.search-wrapper {
  display: flex;
  gap: 1rem;
  max-width: 600px;
  margin: 0 auto;
  justify-content: center;
}

.search-wrapper :deep(.input) {
  flex: 1;
  border-radius: 0.75rem;
}

.ai-suggestion-wrapper {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.ai-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  font-size: 0.9375rem;
  white-space: normal;
  text-align: center;
  max-width: 600px;
}

.ai-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.beta-tag {
  background: linear-gradient(135deg, #0a8961 0%, #066a4e 100%);
  color: #ffffff;
  font-size: 0.625rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-left: 0.25rem;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .ai-button {
    font-size: 0.875rem;
    padding: 0.75rem 1.25rem;
  }
  
  .ai-button span:not(.ai-icon):not(.beta-tag) {
    font-size: 0.8125rem;
  }
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(4px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-overlay-enter-active,
.loading-overlay-leave-active {
  transition: opacity 300ms ease;
}

.loading-overlay-enter-from,
.loading-overlay-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .ai-suggestion-wrapper {
    margin-top: 1.5rem;
  }
  
  .ai-button {
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem;
  }
  
  .beta-tag {
    margin-left: 0;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 4rem 0;
    min-height: 400px;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.125rem;
    margin-bottom: 2rem;
  }
  
  .search-wrapper {
    flex-direction: column;
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
}
</style>
