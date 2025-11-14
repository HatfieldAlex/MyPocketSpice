<template>
  <div id="app">
    <nav class="app-nav">
      <Container>
        <div class="nav-content">
          <router-link to="/recipes" class="nav-logo">
            <span class="logo-text">MyPocketSpice</span>
          </router-link>
          <div class="nav-actions">
            <Button
              v-if="isAuthenticated"
              variant="ghost"
              @click="handleCreateRecipe"
              class="create-recipe-button"
            >
              + Create Recipe
            </Button>
            <div v-if="isAuthenticated" class="user-info">
              <span class="username">{{ user?.username }}</span>
              <Button variant="ghost" size="sm" @click="handleLogout" class="logout-button">
                Logout
              </Button>
            </div>
            <div v-else class="auth-buttons">
              <Button
                variant="ghost"
                @click="openLoginModal('login')"
                class="sign-in-button"
              >
                Sign In
              </Button>
              <Button
                variant="accent"
                @click="openLoginModal('signup')"
                class="sign-up-button"
              >
                Sign Up
              </Button>
            </div>
          </div>
        </div>
      </Container>
    </nav>
    
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <LoginModal 
      :is-open="showLoginModal" 
      :initial-mode="loginModalMode"
      @close="showLoginModal = false" 
      @success="handleAuthSuccess" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Container from './components/ui/Container.vue'
import Button from './components/ui/Button.vue'
import LoginModal from './components/LoginModal.vue'
import { useAuth, initializeAuth } from './composables/useAuth'

const router = useRouter()
const { user, isAuthenticated, logout } = useAuth()
const showLoginModal = ref(false)
const loginModalMode = ref<'login' | 'signup'>('login')

// Initialize auth on app mount
onMounted(async () => {
  // Test backend connection on mount
  const { testBackendConnection, testAuthEndpoint } = await import('@/utils/testBackend')
  
  console.log('=== Backend Connection Test ===')
  const connectionTest = await testBackendConnection()
  console.log('Connection test:', connectionTest)
  
  const authTest = await testAuthEndpoint()
  console.log('Auth endpoint test:', authTest)
  console.log('=== End Backend Tests ===')
  
  // Initialize auth
  initializeAuth()
})

const openLoginModal = (mode: 'login' | 'signup') => {
  loginModalMode.value = mode
  showLoginModal.value = true
}

const handleCreateRecipe = () => {
  if (isAuthenticated.value) {
    // Navigate to create recipe page (you'll need to create this route)
    router.push('/recipes/create')
  } else {
    openLoginModal('login')
  }
}

const handleLogout = async () => {
  await logout()
  router.push('/recipes')
}

const handleAuthSuccess = () => {
  // Refresh page or update state
  showLoginModal.value = false
}
</script>

<style scoped>
.app-nav {
  background: linear-gradient(135deg, #0a8961 0%, #066a4e 100%);
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(10, 10, 10, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  text-decoration: none;
}

.logo-text {
  color: #ffffff;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.username {
  color: #ffffff;
  font-weight: 600;
  font-size: 0.9375rem;
}

.create-recipe-button,
.sign-in-button,
.logout-button {
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.3);
}

.create-recipe-button:hover,
.sign-in-button:hover,
.logout-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.sign-up-button {
  background-color: #ffffff;
  color: #0a8961;
  border-color: #ffffff;
}

.sign-up-button:hover {
  background-color: #fffbfe;
  border-color: #ffffff;
}

.app-main {
  min-height: calc(100vh - 80px);
}

/* Page transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
