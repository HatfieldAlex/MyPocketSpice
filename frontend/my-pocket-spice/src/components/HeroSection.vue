<template>
  <section class="hero-section">
    <Container>
      <div class="hero-content">
        <h1 class="hero-title">My Pocket Spice</h1>
        <p class="hero-subtitle">Discover delicious recipes for every occasion</p>
        
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
  background: linear-gradient(135deg, #fff5fc 0%, #fed1f6 100%);
  padding: 4rem 0;
  border-bottom: 1px solid #fed1f6;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  color: #0a0a0a;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #0a8961 0%, #066a4e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #4a4a4a;
  margin: 0 0 2rem 0;
}

.search-wrapper {
  display: flex;
  gap: 1rem;
  max-width: 600px;
  margin: 0 auto;
}

.search-wrapper :deep(.input) {
  flex: 1;
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .search-wrapper {
    flex-direction: column;
  }
}
</style>
