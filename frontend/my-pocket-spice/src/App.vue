<template>
  <div id="app">
    <nav class="app-nav">
      <Container>
        <div class="nav-content">
          <router-link to="/recipes" class="nav-logo">
            <span class="logo-text">MyPocketSkill</span>
            <span class="logo-accent">Spice</span>
          </router-link>
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
  </div>
</template>

<script setup lang="ts">
import Container from './components/ui/Container.vue'
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
  gap: 0.25rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  text-decoration: none;
}

.logo-text {
  color: #ffffff;
}

.logo-accent {
  color: #fed1f6;
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
