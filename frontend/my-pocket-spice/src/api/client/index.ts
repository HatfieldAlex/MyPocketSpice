/**
 * API Client - Typed endpoints from OpenAPI schema
 */

import { API_CONFIG } from '../config'
import { httpClient } from './http'
import {
  mockPaginatedResponse,
  mockRecipeDetail,
} from './mock-data'
import type {
  PaginatedRecipeListList,
  RecipeDetail,
  RecipeList,
  RecipesListParams,
  RecipesCategoryListParams,
  RecipesSearchListParams,
  RecipeCreate,
} from '../types'

class ApiClient {
  /**
   * GET /api/recipes/
   * Paginated recipe list
   */
  async getRecipes(params?: RecipesListParams): Promise<PaginatedRecipeListList> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockPaginatedResponse(params?.page, params?.page_size))
        }, 300)
      })
    }

    return httpClient.get<PaginatedRecipeListList>('/recipes/', params as Record<string, string | number | undefined>)
  }

  /**
   * GET /api/recipes/{id}/
   * Fetch recipe detail
   */
  async getRecipeById(id: number): Promise<RecipeDetail> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockRecipeDetail)
        }, 300)
      })
    }

    return httpClient.get<RecipeDetail>(`/recipes/${id}/`)
  }

  /**
   * GET /api/recipes/category/{category}/
   * Filter recipes by category
   */
  async getRecipesByCategory(
    params: RecipesCategoryListParams
  ): Promise<PaginatedRecipeListList> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          const filtered = mockPaginatedResponse(params.page, params.page_size)
          resolve(filtered)
        }, 300)
      })
    }

    return httpClient.get<PaginatedRecipeListList>(
      `/recipes/category/${params.category}/`,
      { page: params.page, page_size: params.page_size }
    )
  }

  /**
   * GET /api/recipes/search/
   * Search recipes by title
   */
  async searchRecipes(
    params?: RecipesSearchListParams
  ): Promise<PaginatedRecipeListList> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          const filtered = mockPaginatedResponse(params?.page, params?.page_size)
          if (params?.q) {
            filtered.results = filtered.results.filter((r) =>
              r.title.toLowerCase().includes(params.q!.toLowerCase())
            )
            filtered.count = filtered.results.length
          }
          resolve(filtered)
        }, 300)
      })
    }

    return httpClient.get<PaginatedRecipeListList>('/recipes/search/', params as Record<string, string | number | undefined>)
  }

  /**
   * POST /api/recipes/create/
   * Create a new recipe
   */
  async createRecipe(data: RecipeCreate): Promise<RecipeCreate> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(data)
        }, 500)
      })
    }

    return httpClient.post<RecipeCreate>('/recipes/create/', data)
  }

  /**
   * POST /api/recipes/ai-match/
   * AI-powered recipe matching based on ingredients
   */
  async aiMatchRecipes(ingredients: string): Promise<{ count: number; recipe: RecipeList; justification: string }> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            count: 1,
            recipe: mockPaginatedResponse(1, 1).results[0],
            justification: "With your ingredients, this recipe is a perfect match! Check you have the right amounts, and you're ready to cook."
          })
        }, 2000) // Simulate AI thinking time
      })
    }

    return httpClient.post<{ count: number; recipe: RecipeList; justification: string }>('/recipes/ai-match/', {
      ingredients
    })
  }
}

export const apiClient = new ApiClient()

