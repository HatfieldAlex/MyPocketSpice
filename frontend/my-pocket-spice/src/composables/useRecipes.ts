/**
 * Composable for recipe data fetching and state management
 */

import { ref } from 'vue'
import { apiClient } from '@/api/client'
import type {
  PaginatedRecipeListList,
  RecipeDetail,
  RecipesListParams,
  RecipesCategoryListParams,
  RecipesSearchListParams,
} from '@/api/types'

export function useRecipes() {
  const recipes = ref<PaginatedRecipeListList | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const fetchRecipes = async (params?: RecipesListParams) => {
    loading.value = true
    error.value = null
    try {
      recipes.value = await apiClient.getRecipes(params)
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Failed to fetch recipes')
      console.error('Error fetching recipes:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    recipes,
    loading,
    error,
    fetchRecipes,
  }
}

export function useRecipeDetail() {
  const recipe = ref<RecipeDetail | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const fetchRecipe = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      recipe.value = await apiClient.getRecipeById(id)
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Failed to fetch recipe')
      console.error('Error fetching recipe:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    recipe,
    loading,
    error,
    fetchRecipe,
  }
}

export function useRecipeSearch() {
  const searchResults = ref<PaginatedRecipeListList | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const searchRecipes = async (params?: RecipesSearchListParams) => {
    loading.value = true
    error.value = null
    try {
      searchResults.value = await apiClient.searchRecipes(params)
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Failed to search recipes')
      console.error('Error searching recipes:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    searchResults,
    loading,
    error,
    searchRecipes,
  }
}

export function useRecipesByCategory() {
  const recipes = ref<PaginatedRecipeListList | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const fetchByCategory = async (params: RecipesCategoryListParams) => {
    loading.value = true
    error.value = null
    try {
      recipes.value = await apiClient.getRecipesByCategory(params)
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Failed to fetch recipes by category')
      console.error('Error fetching recipes by category:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    recipes,
    loading,
    error,
    fetchByCategory,
  }
}

