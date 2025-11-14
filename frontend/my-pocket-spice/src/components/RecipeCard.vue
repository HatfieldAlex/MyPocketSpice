<template>
  <Card clickable elevated @click="handleClick">
    <div class="recipe-card-content">
      <div class="recipe-header">
        <h3 class="recipe-title">{{ recipe.title }}</h3>
        <Badge v-if="recipe.category" variant="accent" size="sm">
          {{ recipe.category.name }}
        </Badge>
      </div>
      
      <div class="recipe-meta">
        <div class="meta-item">
          <span class="meta-label">Duration:</span>
          <span class="meta-value">{{ recipe.preparation_duration }} min</span>
        </div>
        <div v-if="recipe.servings" class="meta-item">
          <span class="meta-label">Serves:</span>
          <span class="meta-value">{{ recipe.servings }}</span>
        </div>
        <div v-if="recipe.skill_level" class="meta-item">
          <Badge variant="neutral" size="sm">
            {{ recipe.skill_level.level }}
          </Badge>
        </div>
      </div>
      
      <div class="recipe-footer">
        <time :datetime="recipe.created_at" class="recipe-date">
          {{ formatDate(recipe.created_at) }}
        </time>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import Card from './ui/Card.vue'
import Badge from './ui/Badge.vue'
import type { RecipeList } from '@/api/types'

interface Props {
  recipe: RecipeList
}

const props = defineProps<Props>()
const router = useRouter()

const handleClick = () => {
  router.push(`/recipes/${props.recipe.id}`)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}
</script>

<style scoped>
.recipe-card-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recipe-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.recipe-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0a0a0a;
  margin: 0;
  flex: 1;
  line-height: 1.4;
}

.recipe-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-label {
  font-size: 0.875rem;
  color: #4a4a4a;
}

.meta-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: #0a0a0a;
}

.recipe-footer {
  padding-top: 0.75rem;
  border-top: 1px solid #e8e8e8;
}

.recipe-date {
  font-size: 0.875rem;
  color: #8a8a8a;
}
</style>
