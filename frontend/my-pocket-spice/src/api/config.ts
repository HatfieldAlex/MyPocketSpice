/**
 * API Configuration
 */

export const API_CONFIG = {
  baseURL: process.env.VUE_APP_API_URL || 'https://my-pocket-spice-backend.onrender.com/api',
  useMock: process.env.VUE_APP_USE_MOCK === 'true' || false,
  timeout: 10000,
} as const
