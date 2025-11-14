<template>
  <div class="recipe-detail-page">
    <Container>
      <Button variant="ghost" @click="goBack" class="back-button">
        ← Back to Recipes
      </Button>
      
      <div v-if="loading" class="loading-state">
        <p>Loading recipe...</p>
      </div>
      
      <div v-else-if="error" class="error-state">
        <p>Error: {{ error.message }}</p>
        <Button @click="refetch">Try Again</Button>
      </div>
      
      <div v-else-if="recipe" class="recipe-detail">
        <header class="recipe-header">
          <div class="recipe-title-section">
            <h1 class="recipe-title">{{ recipe.title }}</h1>
            <div class="recipe-badges">
              <Badge v-if="recipe.category" variant="accent">
                {{ recipe.category.name }}
              </Badge>
              <Badge v-if="recipe.skill_level" variant="neutral">
                {{ recipe.skill_level.level }}
              </Badge>
            </div>
          </div>
          
          <div class="recipe-meta">
            <div class="meta-item">
              <span class="meta-icon">⏱</span>
              <span>{{ recipe.preparation_duration }} minutes</span>
            </div>
            <div v-if="recipe.servings" class="meta-item">
              <span class="meta-icon">👥</span>
              <span>Serves {{ recipe.servings }}</span>
            </div>
          </div>
        </header>
        
        <div v-if="recipe.description" class="recipe-description">
          <p>{{ recipe.description }}</p>
        </div>
        
        <div class="recipe-content">
          <section v-if="recipe.recipe_ingredients.length > 0" class="ingredients-section">
            <h2 class="section-title">Ingredients</h2>
            <ul class="ingredients-list">
              <li
                v-for="item in recipe.recipe_ingredients"
                :key="item.id"
                class="ingredient-item"
              >
                <span class="ingredient-quantity">{{ item.quantity }}</span>
                <span class="ingredient-name">{{ item.ingredient.name }}</span>
              </li>
            </ul>
          </section>
          
          <section v-if="recipe.instructions.length > 0" class="instructions-section">
            <h2 class="section-title">Instructions</h2>
            <ol class="instructions-list">
              <li
                v-for="instruction in recipe.instructions"
                :key="instruction.id"
                class="instruction-item"
              >
                <span class="instruction-number">{{ instruction.step_number }}</span>
                <span class="instruction-content">{{ instruction.content }}</span>
              </li>
            </ol>
          </section>
        </div>
      </div>
    </Container>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Container from '@/components/ui/Container.vue'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import { useRecipeDetail } from '@/composables/useRecipes'

const route = useRoute()
const router = useRouter()
const recipeId = computed(() => Number(route.params.id))

const { recipe, loading, error, fetchRecipe } = useRecipeDetail()

const goBack = () => {
  router.push('/recipes')
}

const refetch = () => {
  if (recipeId.value) {
    fetchRecipe(recipeId.value)
  }
}

onMounted(() => {
  if (recipeId.value) {
    fetchRecipe(recipeId.value)
  }
})
</script>

<style scoped>
.recipe-detail-page {
  min-height: 100vh;
  background-color: #ffffff;
  padding: 2rem 0;
}

.back-button {
  margin-bottom: 2rem;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: #4a4a4a;
  gap: 1rem;
}

.recipe-detail {
  max-width: 800px;
  margin: 0 auto;
}

.recipe-header {
  margin-bottom: 2rem;
}

.recipe-title-section {
  margin-bottom: 1.5rem;
}

.recipe-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #0a0a0a;
  margin: 0 0 1rem 0;
  line-height: 1.2;
}

.recipe-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.recipe-meta {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a4a4a;
  font-size: 1rem;
}

.meta-icon {
  font-size: 1.25rem;
}

.recipe-description {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #fffbfe;
  border-radius: 0.75rem;
  border-left: 4px solid #0a8961;
}

.recipe-description p {
  margin: 0;
  color: #0a0a0a;
  line-height: 1.6;
  font-size: 1.125rem;
}

.recipe-content {
  display: grid;
  gap: 3rem;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #0a0a0a;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #fed1f6;
}

.ingredients-section,
.instructions-section {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(10, 10, 10, 0.1), 0 2px 4px -1px rgba(10, 10, 10, 0.06);
}

.ingredients-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ingredient-item {
  display: flex;
  gap: 1rem;
  align-items: baseline;
  padding: 0.75rem;
  background-color: #fffbfe;
  border-radius: 0.5rem;
}

.ingredient-quantity {
  font-weight: 600;
  color: #0a8961;
  min-width: 80px;
}

.ingredient-name {
  color: #0a0a0a;
  flex: 1;
}

.instructions-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.instruction-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.instruction-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background-color: #0a8961;
  color: #ffffff;
  border-radius: 50%;
  font-weight: 600;
  flex-shrink: 0;
}

.instruction-content {
  flex: 1;
  color: #0a0a0a;
  line-height: 1.6;
  padding-top: 0.25rem;
}

@media (max-width: 768px) {
  .recipe-title {
    font-size: 2rem;
  }
  
  .recipe-content {
    gap: 2rem;
  }
  
  .ingredients-section,
  .instructions-section {
    padding: 1.5rem;
  }
}
</style>
