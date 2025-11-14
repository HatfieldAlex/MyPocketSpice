<template>
  <Transition name="modal-fade">
    <div v-if="isOpen" class="login-modal-backdrop" @click.self="handleBackdropClick">
      <div class="login-modal-content">
        <div class="modal-header">
          <h3 class="modal-title">{{ showRegister ? 'Sign Up' : 'Sign In' }}</h3>
          <button class="close-button" @click="closeModal">✕</button>
        </div>
        
        <div class="modal-body">
          <div class="auth-tabs">
            <button 
              :class="['tab-button', { active: !showRegister }]"
              @click="showRegister = false"
            >
              Sign In
            </button>
            <button 
              :class="['tab-button', { active: showRegister }]"
              @click="showRegister = true"
            >
              Sign Up
            </button>
          </div>

          <!-- Login Form -->
          <form v-if="!showRegister" @submit.prevent="handleLogin" class="auth-form">
            <div v-if="authError" class="error-message">{{ authError }}</div>
            
            <div class="form-group">
              <Input
                v-model="loginForm.username"
                placeholder="Enter your username"
                :disabled="isLoading"
                required
              />
            </div>
            
            <div class="form-group">
              <Input
                v-model="loginForm.password"
                type="password"
                placeholder="Enter your password"
                :disabled="isLoading"
                required
              />
            </div>
            
            <div class="form-actions">
              <Button variant="secondary" @click="closeModal" :disabled="isLoading" type="button">
                Cancel
              </Button>
              <Button variant="accent" type="submit" :disabled="isLoading">
                <span v-if="isLoading" class="loading-spinner"></span>
                {{ isLoading ? 'Signing In...' : 'Sign In' }}
              </Button>
            </div>
            <div class="form-footer">
              <p class="switch-text">
                Don't have an account?
                <button type="button" class="switch-link" @click="showRegister = true">
                  Sign up
                </button>
              </p>
            </div>
          </form>

          <!-- Register Form -->
          <form v-else @submit.prevent="handleRegister" class="auth-form">
            <div v-if="authError" class="error-message">{{ authError }}</div>
            
            <div class="form-group">
              <Input
                v-model="registerForm.username"
                placeholder="Choose a username"
                :disabled="isLoading"
                required
              />
            </div>
            
            <div class="form-group">
              <Input
                v-model="registerForm.email"
                type="email"
                placeholder="Email (optional)"
                :disabled="isLoading"
              />
            </div>
            
            <div class="form-group">
              <Input
                v-model="registerForm.password"
                type="password"
                placeholder="Choose a password"
                :disabled="isLoading"
                required
              />
            </div>
            
            <div class="form-group">
              <Input
                v-model="registerForm.password_confirm"
                type="password"
                placeholder="Confirm your password"
                :disabled="isLoading"
                required
              />
            </div>
            
            <div class="form-actions">
              <Button variant="secondary" @click="closeModal" :disabled="isLoading" type="button">
                Cancel
              </Button>
              <Button variant="accent" type="submit" :disabled="isLoading">
                <span v-if="isLoading" class="loading-spinner"></span>
                {{ isLoading ? 'Creating Account...' : 'Sign Up' }}
              </Button>
            </div>
            <div class="form-footer">
              <p class="switch-text">
                Already have an account?
                <button type="button" class="switch-link" @click="showRegister = false">
                  Sign in
                </button>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Button from './ui/Button.vue'
import Input from './ui/Input.vue'
import { useAuth } from '@/composables/useAuth'

interface Props {
  isOpen: boolean
  initialMode?: 'login' | 'signup'
}

const props = withDefaults(defineProps<Props>(), {
  initialMode: 'login',
})

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'success'): void
}>()

const { login, register, isLoading, error: authError } = useAuth()
const showRegister = ref(props.initialMode === 'signup')

const loginForm = ref({
  username: '',
  password: '',
})

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
})

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    loginForm.value = { username: '', password: '' }
    registerForm.value = { username: '', email: '', password: '', password_confirm: '' }
    showRegister.value = props.initialMode === 'signup'
  }
})

watch(() => props.initialMode, (newMode) => {
  if (props.isOpen) {
    showRegister.value = newMode === 'signup'
  }
})

const closeModal = () => {
  emit('close')
}

const handleBackdropClick = () => {
  if (!isLoading.value) {
    closeModal()
  }
}

const handleLogin = async () => {
  const result = await login(loginForm.value)
  if (result.success) {
    emit('success')
    closeModal()
  }
}

const handleRegister = async () => {
  if (registerForm.value.password !== registerForm.value.password_confirm) {
    return
  }
  const result = await register(registerForm.value)
  if (result.success) {
    emit('success')
    closeModal()
  }
}
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.login-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.login-modal-content {
  background-color: #ffffff;
  border-radius: 1rem;
  padding: 2rem;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  transform: translateY(0);
  transition: transform 0.3s ease-out;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-fade-enter-active .login-modal-content,
.modal-fade-leave-active .login-modal-content {
  transition: transform 0.3s ease-out;
}

.modal-fade-enter-from .login-modal-content,
.modal-fade-leave-to .login-modal-content {
  transform: translateY(-20px);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e8e8e8;
  padding-bottom: 1rem;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0a0a0a;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #8a8a8a;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #0a0a0a;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.auth-tabs {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #e8e8e8;
  margin-bottom: 0.5rem;
}

.tab-button {
  flex: 1;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  color: #4a4a4a;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: -2px;
}

.tab-button:hover {
  color: #0a0a0a;
}

.tab-button.active {
  color: #0a8961;
  border-bottom-color: #0a8961;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}


.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 0.5rem;
}

.error-message {
  color: #ff4d4f;
  font-size: 0.875rem;
  padding: 0.75rem;
  background-color: #fff5f5;
  border-radius: 0.5rem;
  border: 1px solid #ffcccc;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.form-footer {
  padding-top: 1rem;
  border-top: 1px solid #e8e8e8;
  margin-top: 0.5rem;
}

.switch-text {
  margin: 0;
  text-align: center;
  color: #4a4a4a;
  font-size: 0.875rem;
}

.switch-link {
  background: none;
  border: none;
  color: #0a8961;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
  margin-left: 0.25rem;
  font-size: inherit;
  font-family: inherit;
}

.switch-link:hover {
  color: #066a4e;
}
</style>

