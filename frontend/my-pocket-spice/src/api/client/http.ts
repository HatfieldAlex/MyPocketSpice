/**
 * HTTP Client
 */

import { API_CONFIG } from '../config'

class HttpClient {
  private baseURL: string
  private accessToken: string | null = null

  constructor(baseURL: string) {
    this.baseURL = baseURL
    // Load token from localStorage on initialization
    this.loadToken()
  }

  setAccessToken(token: string | null) {
    this.accessToken = token
    if (token) {
      localStorage.setItem('access_token', token)
    } else {
      localStorage.removeItem('access_token')
    }
  }

  getAccessToken(): string | null {
    return this.accessToken
  }

  private loadToken() {
    const token = localStorage.getItem('access_token')
    if (token) {
      this.accessToken = token
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    // Log the request for debugging
    console.log(`[HTTP Client] ${options.method || 'GET'} ${url}`)
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    }

    // Add Authorization header if token exists
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
    })

    console.log(`[HTTP Client] Response: ${response.status} ${response.statusText} for ${url}`)

    if (!response.ok) {
      // If unauthorized, clear token
      if (response.status === 401) {
        this.setAccessToken(null)
      }
      
      // Try to get error details from response
      let errorMessage = `HTTP error! status: ${response.status}`
      let errorDetail = ''
      
      try {
        const errorData = await response.json()
        console.error(`[HTTP Client] Error response data:`, errorData)
        if (errorData.detail) {
          errorDetail = errorData.detail
        } else if (errorData.error) {
          errorDetail = errorData.error
        } else if (typeof errorData === 'string') {
          errorDetail = errorData
        } else {
          errorDetail = JSON.stringify(errorData)
        }
      } catch (parseError) {
        // If response is not JSON, try to get text
        try {
          const text = await response.text()
          console.error(`[HTTP Client] Error response text:`, text)
          errorDetail = text || response.statusText || 'Request failed'
        } catch {
          errorDetail = response.statusText || 'Request failed'
        }
      }
      
      if (errorDetail) {
        errorMessage = `${errorMessage} - ${errorDetail}`
      }
      
      console.error(`[HTTP Client] Full error: ${errorMessage} for URL: ${url}`)
      
      const error = new Error(errorMessage)
      ;(error as any).status = response.status
      ;(error as any).url = url
      throw error
    }

    return response.json()
  }

  async get<T>(endpoint: string, params?: Record<string, string | number | undefined>): Promise<T> {
    const queryString = params
      ? '?' + new URLSearchParams(
          Object.entries(params).reduce((acc, [key, value]) => {
            if (value !== undefined && value !== null) {
              acc[key] = String(value)
            }
            return acc
          }, {} as Record<string, string>)
        ).toString()
      : ''
    
    return this.request<T>(`${endpoint}${queryString}`, {
      method: 'GET',
    })
  }

  async post<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }
}

export const httpClient = new HttpClient(API_CONFIG.baseURL)

