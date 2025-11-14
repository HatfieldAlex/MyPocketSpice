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
      </div>
    </Container>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Container from './ui/Container.vue'
import Input from './ui/Input.vue'
import Button from './ui/Button.vue'

const router = useRouter()
const searchQuery = ref('')

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
