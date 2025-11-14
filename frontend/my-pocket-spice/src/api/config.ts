/**
 * API Configuration
 *
 * For this project, we always target the deployed backend on Render.
 * All frontend API calls will go to:
 *   https://my-pocket-spice-backend.onrender.com/api
 */

export const API_CONFIG = {
  // Fixed base URL pointing at the backend root (with /api prefix)
  baseURL: 'https://my-pocket-spice-backend.onrender.com/api',
  // You can still turn on mock mode via env if ever needed
  useMock: process.env.VUE_APP_USE_MOCK === 'true' || false,
  timeout: 10000,
} as const

// Optional debug logs
console.log('[API Config] Base URL:', API_CONFIG.baseURL)
console.log('[API Config] Mock Mode:', API_CONFIG.useMock)
