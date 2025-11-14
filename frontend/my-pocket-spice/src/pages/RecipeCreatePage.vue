<template>
  <div class="recipe-create-page">
    <Container>
      <Button variant="ghost" class="back-button" @click="goBack">
        ← Back to Recipes
      </Button>

      <div class="header">
        <h1 class="title">Create a New Recipe</h1>
        <p class="subtitle">
          Share your favourite dish with the MyPocketSpice community.
        </p>
      </div>

      <div v-if="!isAuthenticated" class="auth-warning">
        <p class="auth-text">
          You need to be signed in to create recipes.
        </p>
        <p class="auth-subtext">
          Please use the <strong>Sign In</strong> or <strong>Sign Up</strong> buttons in the header,
          then come back to this page.
        </p>
      </div>

      <form class="form" @submit.prevent="handleSubmit">
        <div class="form-grid">
          <!-- Title -->
          <div class="form-section">
            <label class="field-label" for="title">Recipe Title</label>
            <Input
              id="title"
              v-model="form.title"
              placeholder="e.g. Creamy Pesto Pasta"
              :disabled="isSubmitting || !isAuthenticated"
              required
            />
          </div>

          <!-- Description -->
          <div class="form-section">
            <label class="field-label" for="description">Description</label>
            <textarea
              id="description"
              v-model="form.description"
              class="textarea"
              placeholder="Describe your recipe and what makes it special..."
              :disabled="isSubmitting || !isAuthenticated"
              rows="4"
              required
            />
          </div>

          <!-- Category & Difficulty -->
          <div class="form-section form-row">
            <div class="field">
              <label class="field-label" for="category">Category</label>
              <select
                id="category"
                v-model="form.category"
                class="select"
                :disabled="isSubmitting || !isAuthenticated"
                required
              >
                <option value="" disabled>Select a category</option>
                <option
                  v-for="cat in categories"
                  :key="cat"
                  :value="cat"
                >
                  {{ cat }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field-label" for="difficulty">Difficulty</label>
              <select
                id="difficulty"
                v-model="form.skill_level_id"
                class="select"
                :disabled="isSubmitting || !isAuthenticated"
                required
              >
                <option value="" disabled>Select difficulty</option>
                <option
                  v-for="level in difficultyOptions"
                  :key="level.id"
                  :value="String(level.id)"
                >
                  {{ level.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- Prep time & servings -->
          <div class="form-section form-row">
            <div class="field">
              <label class="field-label" for="duration">Preparation Time (minutes)</label>
              <Input
                id="duration"
                v-model="form.preparation_duration"
                type="number"
                placeholder="30"
                :disabled="isSubmitting || !isAuthenticated"
                required
              />
            </div>
            <div class="field">
              <label class="field-label" for="servings">Servings (optional)</label>
              <Input
                id="servings"
                v-model="form.servings"
                type="number"
                placeholder="2"
                :disabled="isSubmitting || !isAuthenticated"
              />
            </div>
          </div>

          <!-- Ingredients -->
          <div class="form-section">
            <label class="field-label">Ingredients</label>
            <p class="field-help">
              Add each ingredient with an optional quantity, for example: <em>200g pasta</em>, <em>2 tbsp olive oil</em>.
            </p>
            <div class="ingredients-list">
              <div
                v-for="(ingredient, index) in ingredients"
                :key="ingredient.id"
                class="ingredient-row"
              >
                <Input
                  v-model="ingredient.name"
                  placeholder="Ingredient name"
                  :disabled="isSubmitting || !isAuthenticated"
                  class="ingredient-input"
                  required
                />
                <Input
                  v-model="ingredient.quantity"
                  placeholder="Quantity (optional)"
                  :disabled="isSubmitting || !isAuthenticated"
                  class="ingredient-input"
                />
                <button
                  type="button"
                  class="remove-ingredient"
                  @click="removeIngredient(index)"
                  :disabled="isSubmitting || !isAuthenticated"
                  aria-label="Remove ingredient"
                >
                  ✕
                </button>
              </div>
            </div>
            <Button
              variant="secondary"
              type="button"
              class="add-ingredient-button"
              @click="addIngredient"
              :disabled="isSubmitting || !isAuthenticated"
            >
              + Add Ingredient
            </Button>
          </div>

          <!-- Instructions -->
          <div class="form-section">
            <label class="field-label">Instructions</label>
            <p class="field-help">
              Add each step in the order it should be followed. We'll number them automatically.
            </p>
            <div class="instructions-list">
              <div
                v-for="(step, index) in instructions"
                :key="step.id"
                class="instruction-row"
              >
                <div class="instruction-number">
                  {{ index + 1 }}
                </div>
                <textarea
                  v-model="step.content"
                  class="textarea instruction-textarea"
                  :placeholder="`Step ${index + 1} instructions...`"
                  :disabled="isSubmitting || !isAuthenticated"
                  rows="2"
                  required
                />
                <button
                  type="button"
                  class="remove-instruction"
                  @click="removeInstruction(index)"
                  :disabled="isSubmitting || !isAuthenticated"
                  aria-label="Remove instruction"
                >
                  ✕
                </button>
              </div>
            </div>
            <Button
              variant="secondary"
              type="button"
              class="add-instruction-button"
              @click="addInstruction"
              :disabled="isSubmitting || !isAuthenticated"
            >
              + Add Step
            </Button>
          </div>
        </div>

        <div v-if="errorMessage" class="error-banner">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="success-banner">
          {{ successMessage }}
        </div>

        <div class="form-actions">
          <Button
            variant="secondary"
            type="button"
            @click="goBack"
            :disabled="isSubmitting"
          >
            Cancel
          </Button>
          <Button
            variant="accent"
            type="submit"
            :disabled="isSubmitting || !isAuthenticated"
          >
            <span v-if="isSubmitting" class="loading-spinner"></span>
            {{ isSubmitting ? 'Creating...' : 'Create Recipe' }}
          </Button>
        </div>
      </form>
    </Container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Container from '@/components/ui/Container.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import { apiClient } from '@/api/client'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { isAuthenticated } = useAuth()

const categories = [
  'Italian',
  'Turkish',
  'Asian',
  'Mediterranean',
  'Seafood',
  'Dessert',
  'Vegetarian',
  'Breakfast',
]

const difficultyOptions = [
  { id: 1, label: 'Easy' },
  { id: 2, label: 'Medium' },
]

const form = ref({
  title: '',
  description: '',
  preparation_duration: '',
  servings: '',
  category: '',
  skill_level_id: '',
})

type IngredientFormItem = {
  id: number
  name: string
  quantity: string
}

const ingredients = ref<IngredientFormItem[]>([
  { id: Date.now(), name: '', quantity: '' },
])

type InstructionFormItem = {
  id: number
  content: string
}

const instructions = ref<InstructionFormItem[]>([
  { id: Date.now(), content: '' },
])

const isSubmitting = ref(false)
const errorMessage = ref<string | null>(null)
const successMessage = ref<string | null>(null)

const goBack = () => {
  router.push('/recipes')
}

const addIngredient = () => {
  ingredients.value.push({
    id: Date.now() + Math.random(),
    name: '',
    quantity: '',
  })
}

const removeIngredient = (index: number) => {
  if (ingredients.value.length === 1) {
    ingredients.value[0].name = ''
    ingredients.value[0].quantity = ''
  } else {
    ingredients.value.splice(index, 1)
  }
}

const addInstruction = () => {
  instructions.value.push({
    id: Date.now() + Math.random(),
    content: '',
  })
}

const removeInstruction = (index: number) => {
  if (instructions.value.length === 1) {
    instructions.value[0].content = ''
  } else {
    instructions.value.splice(index, 1)
  }
}

const handleSubmit = async () => {
  if (!isAuthenticated.value) {
    errorMessage.value = 'You must be signed in to create a recipe.'
    return
  }

  if (!form.value.title.trim() || !form.value.description.trim()) {
    errorMessage.value = 'Please fill in the title and description.'
    return
  }

  if (!form.value.category) {
    errorMessage.value = 'Please choose a category.'
    return
  }

  if (!form.value.skill_level_id) {
    errorMessage.value = 'Please choose a difficulty level.'
    return
  }

  // Ensure at least one non-empty instruction
  const hasInstruction = instructions.value.some(
    (step) => step.content.trim().length > 0,
  )
  if (!hasInstruction) {
    errorMessage.value = 'Please add at least one instruction step.'
    return
  }

  isSubmitting.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    const payload: Record<string, unknown> = {
      title: form.value.title.trim(),
      description: form.value.description.trim(),
      preparation_duration: Number(form.value.preparation_duration) || 0,
      servings: form.value.servings
        ? Number(form.value.servings)
        : null,
    }

    // Category (string, case-insensitive lookup on backend)
    if (form.value.category) {
      payload.category = form.value.category
    }

    // Difficulty (skill level id)
    if (form.value.skill_level_id) {
      payload.skill_level_id = Number(form.value.skill_level_id)
    }

    // Ingredients array
    const cleanedIngredients = ingredients.value
      .filter((i) => i.name.trim())
      .map((i) => ({
        name: i.name.trim(),
        quantity: i.quantity.trim(),
      }))

    if (cleanedIngredients.length > 0) {
      payload.ingredients = cleanedIngredients
    }

    // Instructions array
    const cleanedInstructions = instructions.value
      .map((step, index) => ({
        step_number: index + 1,
        content: step.content.trim(),
      }))
      .filter((step) => step.content.length > 0)

    if (cleanedInstructions.length > 0) {
      payload.instructions = cleanedInstructions
    }

    const created = await apiClient.createRecipe(payload)

    successMessage.value = 'Recipe created successfully! Redirecting...'

    // If backend returns an id, navigate to the detail page
    const createdId = (created as any).id
    if (createdId) {
      setTimeout(() => {
        router.push(`/recipes/${createdId}`)
      }, 800)
    } else {
      // Fallback: go back to the list
      setTimeout(() => {
        router.push('/recipes')
      }, 800)
    }
  } catch (err) {
    if (err instanceof Error) {
      const anyErr = err as any
      if (anyErr.status === 400) {
        errorMessage.value =
          'There was a problem with your recipe data. Please check the fields and try again.'
      } else if (anyErr.status === 401) {
        errorMessage.value =
          'Your session has expired or you are not authenticated. Please sign in again.'
      } else if (anyErr.status === 403) {
        errorMessage.value =
          'You do not have permission to create recipes.'
      } else {
        errorMessage.value = err.message || 'Failed to create recipe.'
      }
    } else {
      errorMessage.value = 'Failed to create recipe.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.recipe-create-page {
  min-height: 100vh;
  background-color: #ffffff;
  padding: 2rem 0 3rem;
}

.back-button {
  margin-bottom: 1.5rem;
}

.header {
  margin-bottom: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #0a0a0a;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  margin: 0;
  color: #4a4a4a;
  font-size: 0.975rem;
}

.auth-warning {
  margin-bottom: 1.5rem;
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  background-color: #fffbfe;
  border-left: 4px solid #0a8961;
}

.auth-text {
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  color: #0a0a0a;
}

.auth-subtext {
  margin: 0;
  color: #4a4a4a;
  font-size: 0.9rem;
}

.form {
  max-width: 720px;
  margin-top: 1rem;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #0a0a0a;
}

.select {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: #0a0a0a;
  background-color: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 0.5rem;
  outline: none;
  transition: border-color 200ms ease, box-shadow 200ms ease;
  font-family: inherit;
  appearance: none;
  background-image: linear-gradient(45deg, transparent 50%, #0a8961 50%),
    linear-gradient(135deg, #0a8961 50%, transparent 50%);
  background-position: calc(100% - 18px) calc(50% - 4px),
    calc(100% - 13px) calc(50% - 4px);
  background-size: 5px 5px, 5px 5px;
  background-repeat: no-repeat;
}

.select:focus {
  border-color: #0a8961;
  box-shadow: 0 0 0 3px rgba(10, 137, 97, 0.1);
}

.textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: #0a0a0a;
  background-color: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 0.5rem;
  outline: none;
  transition: border-color 200ms ease, box-shadow 200ms ease;
  font-family: inherit;
  resize: vertical;
}

.textarea:focus {
  border-color: #0a8961;
  box-shadow: 0 0 0 3px rgba(10, 137, 97, 0.1);
}

.ingredients-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.ingredient-row {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 2fr) auto;
  gap: 0.5rem;
  align-items: center;
}

.ingredient-input {
  width: 100%;
}

.remove-ingredient {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 999px;
  border: none;
  background-color: #fffbfe;
  color: #b91c1c;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
  transition: background-color 150ms ease, transform 150ms ease, box-shadow 150ms ease;
}

.remove-ingredient:hover {
  background-color: #fee2e2;
  box-shadow: 0 2px 4px rgba(185, 28, 28, 0.25);
  transform: translateY(-1px);
}

.remove-ingredient:disabled {
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
  transform: none;
}

.add-ingredient-button {
  margin-top: 0.5rem;
}

.field-help {
  margin: 0 0 0.5rem 0;
  font-size: 0.85rem;
  color: #6b7280;
}

.instructions-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.instruction-row {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 0.5rem;
  align-items: flex-start;
}

.instruction-number {
  width: 2rem;
  height: 2rem;
  border-radius: 999px;
  background-color: #0a8961;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.instruction-textarea {
  min-height: 2.5rem;
}

.remove-instruction {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 999px;
  border: none;
  background-color: #fffbfe;
  color: #b91c1c;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
  transition: background-color 150ms ease, transform 150ms ease, box-shadow 150ms ease;
}

.remove-instruction:hover {
  background-color: #fee2e2;
  box-shadow: 0 2px 4px rgba(185, 28, 28, 0.25);
  transform: translateY(-1px);
}

.remove-instruction:disabled {
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
  transform: none;
}

.add-instruction-button {
  margin-top: 0.5rem;
}

.error-banner {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  background-color: #fff5f5;
  color: #b91c1c;
  border: 1px solid #fecaca;
  font-size: 0.9rem;
}

.success-banner {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  background-color: #ecfdf3;
  color: #166534;
  border: 1px solid #bbf7d0;
  font-size: 0.9rem;
}

.form-actions {
  margin-top: 1.75rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.loading-spinner {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid #ffffff;
  border-radius: 50%;
  width: 1em;
  height: 1em;
  animation: spin 1s linear infinite;
  display: inline-block;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>


