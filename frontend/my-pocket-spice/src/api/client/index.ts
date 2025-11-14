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
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  LogoutRequest,
  User,
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

  /**
   * POST /api/auth/register/
   * Register a new user
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            user: {
              id: 1,
              username: data.username,
              email: data.email || '',
              first_name: data.first_name || '',
              last_name: data.last_name || '',
              date_joined: new Date().toISOString(),
            },
            access: 'mock_access_token',
            refresh: 'mock_refresh_token',
          })
        }, 500)
      })
    }

    return httpClient.post<AuthResponse>('/auth/register/', data)
  }

  /**
   * POST /api/auth/login/
   * Login user
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            user: {
              id: 1,
              username: data.username,
              email: 'test@example.com',
              first_name: '',
              last_name: '',
              date_joined: new Date().toISOString(),
            },
            access: 'mock_access_token',
            refresh: 'mock_refresh_token',
          })
        }, 500)
      })
    }

    return httpClient.post<AuthResponse>('/auth/login/', data)
  }

  /**
   * POST /api/auth/logout/
   * Logout user
   */
  async logout(data: LogoutRequest): Promise<{ detail: string }> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({ detail: 'Successfully logged out.' })
        }, 300)
      })
    }

    return httpClient.post<{ detail: string }>('/auth/logout/', data)
  }

  /**
   * GET /api/auth/me/
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User> {
    if (API_CONFIG.useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            id: 1,
            username: 'testuser',
            email: 'test@example.com',
            first_name: '',
            last_name: '',
            date_joined: new Date().toISOString(),
          })
        }, 300)
      })
    }

    return httpClient.get<User>('/auth/me/')
  }
}

export const apiClient = new ApiClient()

