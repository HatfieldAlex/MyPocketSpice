/**
 * Composable for recipe data fetching and state management
 */

import { ref } from 'vue'
import { apiClient } from '@/api/client'
import { useAuth } from './useAuth'
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
  const { user } = useAuth()

  const fetchByCategory = async (params: RecipesCategoryListParams) => {
    loading.value = true
    error.value = null
    try {
      // Handle "mine" category specially - filter by current user's recipes
      // Note: The backend doesn't have a /recipes/category/mine/ endpoint,
      // so we fetch all recipes and filter client-side
      if (params.category === 'mine') {
        if (!user.value) {
          throw new Error('You must be logged in to view your recipes')
        }
        
        // Fetch all recipes (with pagination if needed)
        const pageSize = params.page_size || 9
        const page = params.page || 1
        
        // Fetch a large batch to filter client-side
        // In production, you'd want a backend endpoint like /recipes/mine/
        const allRecipes = await apiClient.getRecipes({ page: 1, page_size: 1000 })
        
        const userRecipes = allRecipes.results.filter(
          (recipe) => recipe.author?.id === user.value?.id
        )
        
        const startIndex = (page - 1) * pageSize
        const endIndex = startIndex + pageSize
        
        recipes.value = {
          count: userRecipes.length,
          next: endIndex < userRecipes.length ? 'next' : null,
          previous: page > 1 ? 'previous' : null,
          results: userRecipes.slice(startIndex, endIndex),
        }
      } else {
        recipes.value = await apiClient.getRecipesByCategory(params)
      }
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Failed to fetch recipes by category')
      console.error('Error fetching recipes by category:', err)
      if ((err as any).url) {
        console.error('Failed URL:', (err as any).url)
      }
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

