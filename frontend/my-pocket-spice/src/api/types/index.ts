/**
 * TypeScript types generated from OpenAPI schema
 * Single source of truth: schema.yaml
 */

// ============================================
// Component Schemas
// ============================================

export interface Category {
  id: number
  name: string
}

export interface Ingredient {
  id: number
  name: string
}

export interface SkillLevel {
  id: number
  level: string
}

export interface Instruction {
  id: number
  step_number: number
  content: string
}

export interface RecipeIngredient {
  id: number
  ingredient: Ingredient
  quantity: string
}

export interface UserInfo {
  id: number
  username: string
}

// ============================================
// Recipe Types
// ============================================

export interface RecipeList {
  id: number
  title: string
  preparation_duration: number
  servings: number | null
  category: Category
  skill_level: SkillLevel
  created_at: string
  author?: UserInfo | null
}

export interface RecipeDetail {
  id: number
  title: string
  category: Category
  description: string
  preparation_duration: number
  servings: number | null
  skill_level: SkillLevel
  created_at: string
  instructions: Instruction[]
  recipe_ingredients: RecipeIngredient[]
  author?: UserInfo | null
}

// ============================================
// Pagination Types
// ============================================

export interface PaginatedRecipeListList {
  count: number
  next: string | null
  previous: string | null
  results: RecipeList[]
}

// ============================================
// Request Types
// ============================================

export interface RecipeCreate {
  title: string
  description: string
  preparation_duration: number
  servings?: number | null
  skill_level_id?: number | null
  category?: string
  ingredients?: Array<Record<string, unknown>>
  instructions?: Array<Record<string, unknown>>
}

// ============================================
// API Request Parameters
// ============================================

export interface RecipesListParams {
  page?: number
  page_size?: number
}

export interface RecipesCategoryListParams {
  category: string
  page?: number
  page_size?: number
}

export interface RecipesSearchListParams {
  q?: string
  page?: number
  page_size?: number
}

// ============================================
// Authentication Types
// ============================================

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  date_joined: string
}

export interface AuthResponse {
  user: User
  access: string
  refresh: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
  password_confirm: string
  email?: string
  first_name?: string
  last_name?: string
}

export interface LogoutRequest {
  refresh: string
}

