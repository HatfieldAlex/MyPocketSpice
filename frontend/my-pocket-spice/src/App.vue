<template>
  <div id="app">
    <header>
      <h1>My Pocket Spice</h1>
      <p class="subtitle">Recipe Collection</p>
    </header>
    
    <div v-if="loading" class="loading">
      Loading recipes...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else class="recipes-container">
      <article 
        v-for="recipe in recipes" 
        :key="recipe.id" 
        class="recipe-card"
      >
        <h2 class="recipe-title">{{ recipe.title }}</h2>
        
        <p v-if="recipe.description" class="recipe-description">
          {{ recipe.description }}
        </p>
        
        <div class="recipe-section">
          <h3>Ingredients</h3>
          <p class="recipe-content">{{ recipe.ingredients }}</p>
        </div>
        
        <div class="recipe-section">
          <h3>Instructions</h3>
          <p class="recipe-content">{{ recipe.instructions }}</p>
        </div>
        
        <footer class="recipe-footer">
          <time :datetime="recipe.created_at">
            {{ formatDate(recipe.created_at) }}
          </time>
        </footer>
      </article>
      
      <div v-if="recipes.length === 0" class="empty-state">
        No recipes found.
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const recipes = ref([])
    const loading = ref(true)
    const error = ref(null)
    const apiUrl = 'https://my-pocket-spice-backend.onrender.com/api/recipes/'

    const fetchRecipes = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await fetch(apiUrl)
        
        if (!response.ok) {
          throw new Error(`Failed to fetch recipes: ${response.status}`)
        }
        
        const data = await response.json()
        recipes.value = data
      } catch (err) {
        error.value = err.message || 'An error occurred while fetching recipes'
        console.error('Error fetching recipes:', err)
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      fetchRecipes()
    })

    return {
      recipes,
      loading,
      error,
      formatDate
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
  background-color: #f5f5f5;
  min-height: 100vh;
}

header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
}

header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.loading, .error, .empty-state {
  text-align: center;
  padding: 3rem;
  font-size: 1.1rem;
  color: #7f8c8d;
}

.error {
  color: #e74c3c;
  background-color: #fee;
  border-radius: 8px;
  border: 1px solid #fcc;
}

.recipes-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.recipe-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.recipe-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.recipe-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #3498db;
}

.recipe-description {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.recipe-section {
  margin-bottom: 1.5rem;
}

.recipe-section h3 {
  font-size: 1.2rem;
  color: #34495e;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.recipe-content {
  color: #555;
  line-height: 1.6;
  white-space: pre-wrap;
}

.recipe-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
  font-size: 0.9rem;
  color: #95a5a6;
}

time {
  font-style: italic;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #95a5a6;
  font-size: 1.2rem;
}

@media (max-width: 600px) {
  #app {
    padding: 1rem 0.5rem;
  }

  header h1 {
    font-size: 2rem;
  }

  .recipe-card {
    padding: 1.5rem;
  }
}
</style>
