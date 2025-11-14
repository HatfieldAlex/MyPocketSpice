<template>
  <div class="category-filter">
    <div class="category-list">
      <button
        v-for="category in categories"
        :key="category"
        :class="['category-box', { active: isCategoryActive(category) }]"
        @click="handleCategoryClick(category)"
      >
        {{ category }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps<{
  selectedCategory: string | null
}>()

const emit = defineEmits<{
  categorySelected: [category: string | null]
}>()

const categories = ['All', 'Italian', 'Asian', 'Vegetarian', 'Seafood', 'Dessert', 'Breakfast']

const isCategoryActive = (category: string): boolean => {
  if (category === 'All') {
    return props.selectedCategory === null
  }
  return props.selectedCategory === category
}

const handleCategoryClick = (category: string) => {
  const selected = category === 'All' ? null : category
  emit('categorySelected', selected)
}
</script>

<style scoped>
.category-filter {
  width: 100%;
  padding: 1.5rem 0;
}

.category-list {
  display: flex;
  gap: 0.75rem;
  overflow-x: auto;
  padding: 0.5rem 0;
  scrollbar-width: thin;
  scrollbar-color: #fed1f6 transparent;
}

.category-list::-webkit-scrollbar {
  height: 6px;
}

.category-list::-webkit-scrollbar-track {
  background: transparent;
}

.category-list::-webkit-scrollbar-thumb {
  background-color: #fed1f6;
  border-radius: 3px;
}

.category-box {
  flex-shrink: 0;
  padding: 0.75rem 1.5rem;
  border-radius: 2rem;
  border: 1px solid #fed1f6;
  background-color: #fed1f6;
  color: #0a0a0a;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px 0 rgba(254, 209, 246, 0.3), 0 1px 2px 0 rgba(254, 209, 246, 0.2);
  white-space: nowrap;
}

.category-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(254, 209, 246, 0.4), 0 2px 4px -1px rgba(254, 209, 246, 0.3);
  background-color: #fdb8f0;
}

.category-box.active {
  background-color: #0a8961;
  color: #ffffff;
  border-color: #0a8961;
  box-shadow: 0 4px 6px -1px rgba(10, 137, 97, 0.2), 0 2px 4px -1px rgba(10, 137, 97, 0.1);
}

.category-box.active:hover {
  background-color: #066a4e;
  border-color: #066a4e;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px -1px rgba(10, 137, 97, 0.25), 0 4px 6px -1px rgba(10, 137, 97, 0.15);
}

@media (min-width: 768px) {
  .category-list {
    justify-content: center;
    flex-wrap: wrap;
    overflow-x: visible;
  }
  
  .category-filter {
    padding: 2rem 0;
  }
}

@media (max-width: 640px) {
  .category-box {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }
}
</style>

