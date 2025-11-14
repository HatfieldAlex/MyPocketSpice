<template>
  <div class="recipe-list-page">
    <HeroSection />
    
    <Container>
      <CategoryFilter
        :selected-category="selectedCategory"
        @category-selected="handleCategorySelected"
      />
      
      <div v-if="isLoading" class="loading-state">
        <p>Loading recipes...</p>
      </div>
      
      <div v-else-if="displayError" class="error-state">
        <p>Error: {{ displayError?.message }}</p>
        <Button @click="refetch">Try Again</Button>
      </div>
      
      <div v-else-if="displayRecipes && displayRecipes.results.length === 0" class="empty-state">
        <p>No recipes found.</p>
      </div>
      
      <div v-else-if="displayRecipes" class="recipes-content">
        <div class="recipes-grid">
          <RecipeCard
            v-for="recipe in displayRecipes.results"
            :key="recipe.id"
            :recipe="recipe"
          />
        </div>
        
        <div v-if="displayRecipes.count > displayRecipes.results.length" class="pagination">
          <Button
            v-if="displayRecipes.previous"
            variant="secondary"
            @click="loadPrevious"
          >
            Previous
          </Button>
          <span class="pagination-info">
            Page {{ currentPage }} of {{ totalPages }}
          </span>
          <Button
            v-if="displayRecipes.next"
            variant="accent"
            @click="loadNext"
          >
            Next
          </Button>
        </div>
      </div>
    </Container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Container from '@/components/ui/Container.vue'
import Button from '@/components/ui/Button.vue'
import RecipeCard from '@/components/RecipeCard.vue'
import HeroSection from '@/components/HeroSection.vue'
import CategoryFilter from '@/components/CategoryFilter.vue'
import { useRecipes, useRecipeSearch, useRecipesByCategory } from '@/composables/useRecipes'

const route = useRoute()
const currentPage = ref(1)
const pageSize = ref(9)
const selectedCategory = ref<string | null>(null)

const searchQuery = computed(() => route.query.q as string | undefined)
const isSearching = computed(() => !!searchQuery.value)

const { recipes, loading, error, fetchRecipes } = useRecipes()
const { searchResults, loading: searchLoading, error: searchError, searchRecipes } = useRecipeSearch()
const { recipes: categoryRecipes, loading: categoryLoading, error: categoryError, fetchByCategory } = useRecipesByCategory()

const isLoading = computed(() => {
  if (isSearching.value) return searchLoading.value
  if (selectedCategory.value) return categoryLoading.value
  return loading.value
})

const displayError = computed(() => {
  if (isSearching.value) return searchError.value
  if (selectedCategory.value) return categoryError.value
  return error.value
})

const displayRecipes = computed(() => {
  if (isSearching.value) return searchResults.value
  if (selectedCategory.value) return categoryRecipes.value
  return recipes.value
})

const totalPages = computed(() => {
  if (!displayRecipes.value) return 0
  return Math.ceil(displayRecipes.value.count / pageSize.value)
})

const handleCategorySelected = (category: string | null) => {
  selectedCategory.value = category
  currentPage.value = 1
  refetch()
}

const refetch = async () => {
  if (isSearching.value) {
    await searchRecipes({ q: searchQuery.value, page: currentPage.value, page_size: pageSize.value })
  } else if (selectedCategory.value) {
    await fetchByCategory({ category: selectedCategory.value, page: currentPage.value, page_size: pageSize.value })
  } else {
    await fetchRecipes({ page: currentPage.value, page_size: pageSize.value })
  }
}

const loadNext = () => {
  currentPage.value++
  refetch()
}

const loadPrevious = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    refetch()
  }
}

onMounted(() => {
  const page = route.query.page ? Number(route.query.page) : 1
  currentPage.value = page
  
  if (isSearching.value) {
    searchRecipes({ q: searchQuery.value, page, page_size: pageSize.value })
  } else {
    fetchRecipes({ page, page_size: pageSize.value })
  }
})

watch(() => route.query, () => {
  const page = route.query.page ? Number(route.query.page) : 1
  currentPage.value = page
  
  if (isSearching.value) {
    searchRecipes({ q: searchQuery.value, page, page_size: pageSize.value })
  } else if (selectedCategory.value) {
    fetchByCategory({ category: selectedCategory.value, page, page_size: pageSize.value })
  } else {
    fetchRecipes({ page, page_size: pageSize.value })
  }
})
</script>

<style scoped>
.recipe-list-page {
  min-height: 100vh;
  background-color: #ffffff;
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: #4a4a4a;
}

.error-state {
  gap: 1rem;
}

.recipes-content {
  padding: 2rem 0;
}

.recipes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 2rem 0;
}

.pagination-info {
  color: #4a4a4a;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .recipes-grid {
    grid-template-columns: 1fr;
  }
}
</style>
