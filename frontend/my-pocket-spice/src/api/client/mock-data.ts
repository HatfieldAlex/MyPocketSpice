/**
 * Mock data matching OpenAPI schema types
 */

import type {
  PaginatedRecipeListList,
  RecipeDetail,
  RecipeList,
  Category,
  SkillLevel,
  Instruction,
  RecipeIngredient,
  Ingredient,
} from '../types'

const mockCategory: Category = {
  id: 1,
  name: 'Dinner',
}

const mockSkillLevel: SkillLevel = {
  id: 1,
  level: 'Intermediate',
}

const mockIngredient1: Ingredient = {
  id: 1,
  name: 'Fresh basil',
}

const mockIngredient2: Ingredient = {
  id: 2,
  name: 'Mozzarella cheese',
}

const mockRecipeIngredient1: RecipeIngredient = {
  id: 1,
  ingredient: mockIngredient1,
  quantity: '1 cup',
}

const mockRecipeIngredient2: RecipeIngredient = {
  id: 2,
  ingredient: mockIngredient2,
  quantity: '200g',
}

const mockInstruction1: Instruction = {
  id: 1,
  step_number: 1,
  content: 'Preheat oven to 425°F (220°C).',
}

const mockInstruction2: Instruction = {
  id: 2,
  step_number: 2,
  content: 'Roll out pizza dough on a floured surface.',
}

const mockInstruction3: Instruction = {
  id: 3,
  step_number: 3,
  content: 'Add toppings and bake for 12-15 minutes until golden.',
}

export const mockRecipeList: RecipeList[] = [
  {
    id: 1,
    title: 'Classic Margherita Pizza',
    preparation_duration: 30,
    servings: 4,
    category: mockCategory,
    skill_level: mockSkillLevel,
    created_at: '2025-11-13T19:56:22.363858Z',
  },
  {
    id: 2,
    title: 'Creamy Mushroom Risotto',
    preparation_duration: 45,
    servings: 3,
    category: { id: 2, name: 'Main Course' },
    skill_level: { id: 2, level: 'Advanced' },
    created_at: '2025-11-12T15:30:00.000000Z',
  },
  {
    id: 3,
    title: 'Fresh Garden Salad',
    preparation_duration: 15,
    servings: 2,
    category: { id: 3, name: 'Salad' },
    skill_level: { id: 3, level: 'Beginner' },
    created_at: '2025-11-11T10:20:00.000000Z',
  },
]

export const mockRecipeDetail: RecipeDetail = {
  id: 1,
  title: 'Classic Margherita Pizza',
  category: mockCategory,
  description: 'A classic Italian pizza with fresh tomatoes, mozzarella, and basil. Simple, fresh, and delicious.',
  preparation_duration: 30,
  servings: 4,
  skill_level: mockSkillLevel,
  created_at: '2025-11-13T19:56:22.363858Z',
  instructions: [mockInstruction1, mockInstruction2, mockInstruction3],
  recipe_ingredients: [mockRecipeIngredient1, mockRecipeIngredient2],
}

export const mockPaginatedResponse = (
  page: number = 1,
  pageSize: number = 10
): PaginatedRecipeListList => {
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const results = mockRecipeList.slice(start, end)
  const total = mockRecipeList.length

  return {
    count: total,
    next: end < total ? `?page=${page + 1}&page_size=${pageSize}` : null,
    previous: page > 1 ? `?page=${page - 1}&page_size=${pageSize}` : null,
    results,
  }
}

