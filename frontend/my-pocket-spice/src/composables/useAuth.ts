/**
 * Authentication Composable
 * Manages user authentication state and operations
 */

import { ref, computed } from 'vue'
import { apiClient } from '@/api/client'
import { httpClient } from '@/api/client/http'
import type { User, LoginRequest, RegisterRequest } from '@/api/types'

const user = ref<User | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)

// Initialize auth check - call this from App.vue onMounted instead
export async function initializeAuth() {
  const token = httpClient.getAccessToken()
  if (token) {
    try {
      const currentUser = await apiClient.getCurrentUser()
      user.value = currentUser
    } catch (err) {
      // Token might be invalid, clear it
      console.warn('[Auth] Failed to load user from token:', err)
      httpClient.setAccessToken(null)
      user.value = null
    }
  }
}

export function useAuth() {
  const isAuthenticated = computed(() => !!user.value)

  const login = async (credentials: LoginRequest) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await apiClient.login(credentials)
      httpClient.setAccessToken(response.access)
      localStorage.setItem('refresh_token', response.refresh)
      user.value = response.user
      return { success: true }
    } catch (err) {
      // Improve login error messaging
      if (err instanceof Error) {
        const anyErr = err as any
        if (anyErr.status === 401) {
          error.value = 'Invalid username or password.'
        } else if (anyErr.status === 404) {
          error.value = 'Login service is unavailable (404). Please check the backend API URL and deployment.'
        } else {
          error.value = err.message || 'Login failed'
        }
      } else {
        error.value = 'Login failed'
      }
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const register = async (data: RegisterRequest) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await apiClient.register(data)
      httpClient.setAccessToken(response.access)
      localStorage.setItem('refresh_token', response.refresh)
      user.value = response.user
      return { success: true }
    } catch (err) {
      // Improve registration error messaging
      if (err instanceof Error) {
        const anyErr = err as any
        if (anyErr.status === 400) {
          // Backend will return validation errors in the response body
          error.value = err.message || 'Please check your details and try again.'
        } else if (anyErr.status === 404) {
          error.value =
            'Sign up is currently unavailable (signup endpoint not found – 404). Please ensure the backend is deployed with authentication routes.'
        } else {
          error.value = err.message || 'Registration failed'
        }
      } else {
        error.value = 'Registration failed'
      }
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    isLoading.value = true
    error.value = null
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        await apiClient.logout({ refresh: refreshToken })
      }
    } catch (err) {
      // Continue with logout even if API call fails
      console.error('Logout error:', err)
    } finally {
      httpClient.setAccessToken(null)
      localStorage.removeItem('refresh_token')
      user.value = null
      isLoading.value = false
    }
  }

  const checkAuth = async () => {
    const token = httpClient.getAccessToken()
    if (token && !user.value) {
      try {
        const currentUser = await apiClient.getCurrentUser()
        user.value = currentUser
      } catch (err) {
        httpClient.setAccessToken(null)
        user.value = null
      }
    }
  }

  return {
    user: computed(() => user.value),
    isAuthenticated,
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    login,
    register,
    logout,
    checkAuth,
  }
}

