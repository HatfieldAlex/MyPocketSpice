/// <reference types="vite/client" />

declare namespace NodeJS {
  interface ProcessEnv {
    readonly VUE_APP_API_URL?: string
    readonly VUE_APP_USE_MOCK?: string
  }
}
