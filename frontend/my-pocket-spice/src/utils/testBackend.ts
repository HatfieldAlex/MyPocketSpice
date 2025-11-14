/**
 * Utility to test backend connectivity
 */

import { API_CONFIG } from '@/api/config'

export async function testBackendConnection(): Promise<{
  success: boolean
  message: string
  url?: string
}> {
  const testUrl = `${API_CONFIG.baseURL}/recipes/`
  
  try {
    console.log(`[Backend Test] Testing connection to: ${testUrl}`)
    const response = await fetch(testUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    console.log(`[Backend Test] Response status: ${response.status}`)
    
    if (response.ok) {
      return {
        success: true,
        message: `Backend is reachable! Status: ${response.status}`,
        url: testUrl,
      }
    } else {
      return {
        success: false,
        message: `Backend responded with status: ${response.status}`,
        url: testUrl,
      }
    }
  } catch (error) {
    console.error('[Backend Test] Connection failed:', error)
    return {
      success: false,
      message: error instanceof Error ? error.message : 'Unknown error',
      url: testUrl,
    }
  }
}

export async function testAuthEndpoint(): Promise<{
  success: boolean
  message: string
  url?: string
}> {
  const testUrl = `${API_CONFIG.baseURL}/auth/register/`
  
  try {
    console.log(`[Backend Test] Testing auth endpoint: ${testUrl}`)
    const response = await fetch(testUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: 'test',
        password: 'test',
        password_confirm: 'test',
      }),
    })
    
    console.log(`[Backend Test] Auth endpoint status: ${response.status}`)
    
    // 400 is expected (validation error), 404 means endpoint doesn't exist
    if (response.status === 404) {
      return {
        success: false,
        message: 'Auth endpoint not found (404). Backend may not be deployed with auth routes.',
        url: testUrl,
      }
    } else if (response.status === 400) {
      return {
        success: true,
        message: 'Auth endpoint exists! (Got 400 validation error, which is expected)',
        url: testUrl,
      }
    } else {
      return {
        success: response.ok,
        message: `Auth endpoint responded with status: ${response.status}`,
        url: testUrl,
      }
    }
  } catch (error) {
    console.error('[Backend Test] Auth endpoint test failed:', error)
    return {
      success: false,
      message: error instanceof Error ? error.message : 'Unknown error',
      url: testUrl,
    }
  }
}

