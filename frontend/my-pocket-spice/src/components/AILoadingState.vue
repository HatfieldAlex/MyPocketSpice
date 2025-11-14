<template>
  <div class="ai-loading">
    <div class="loading-content">
      <div class="thinking-icon">
        <div class="pulse-dot"></div>
        <div class="pulse-dot"></div>
        <div class="pulse-dot"></div>
      </div>
      <p class="thinking-text">
        Thinking<span class="dots">{{ animatedDots }}</span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const animatedDots = ref('')
let intervalId: number | null = null

onMounted(() => {
  let dotCount = 0
  intervalId = window.setInterval(() => {
    dotCount = (dotCount + 1) % 4
    animatedDots.value = '.'.repeat(dotCount)
  }, 500)
})

onUnmounted(() => {
  if (intervalId !== null) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.ai-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  min-height: 200px;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.thinking-icon {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.pulse-dot {
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, #fed1f6 0%, #0a8961 100%);
  border-radius: 50%;
  animation: pulse 1.4s ease-in-out infinite;
}

.pulse-dot:nth-child(1) {
  animation-delay: 0s;
}

.pulse-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.pulse-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.7;
  }
}

.thinking-text {
  font-size: 1.25rem;
  font-weight: 500;
  color: #0a0a0a;
  margin: 0;
  background: linear-gradient(135deg, #0a8961 0%, #066a4e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.dots {
  display: inline-block;
  min-width: 1ch;
  text-align: left;
}

@media (max-width: 640px) {
  .thinking-text {
    font-size: 1rem;
  }
  
  .pulse-dot {
    width: 10px;
    height: 10px;
  }
}
</style>

