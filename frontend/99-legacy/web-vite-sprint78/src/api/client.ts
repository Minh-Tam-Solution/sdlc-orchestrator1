/**
 * File: frontend/web/src/api/client.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Axios HTTP client with authentication and error handling for SDLC Orchestrator API.
 * Implements JWT token refresh, request/response interceptors, and automatic retry logic.
 */

import axios, { AxiosError, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios'

/**
 * Base API URL from environment or default to Vite proxy
 */
const API_BASE_URL = import.meta.env['VITE_API_URL'] ?? '/api/v1'

/**
 * Axios client instance with default configuration
 *
 * Features:
 * - Base URL: /api/v1 (proxied to backend in dev)
 * - Timeout: 30 seconds
 * - JSON content type
 * - Automatic token injection
 * - Token refresh on 401
 */
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Token storage keys
 */
const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

/**
 * Get access token from localStorage
 */
export function getAccessToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * Get refresh token from localStorage
 */
export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

/**
 * Set access token in localStorage
 */
export function setAccessToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

/**
 * Set refresh token in localStorage
 */
export function setRefreshToken(token: string): void {
  localStorage.setItem(REFRESH_TOKEN_KEY, token)
}

/**
 * Set both access and refresh tokens
 */
export function setTokens(accessToken: string, refreshToken: string): void {
  setAccessToken(accessToken)
  setRefreshToken(refreshToken)
}

/**
 * Clear all tokens from localStorage
 */
export function clearTokens(): void {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

/**
 * Request interceptor - Inject JWT token into Authorization header
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = getAccessToken()

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

/**
 * Response interceptor - Handle token refresh on 401
 */
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }

    // If 401 and not already retried, attempt token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = getRefreshToken()

      if (!refreshToken) {
        // No refresh token, redirect to login
        clearTokens()
        window.location.href = '/login'
        return Promise.reject(error)
      }

      try {
        // Call refresh endpoint
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        })

        const { access_token, refresh_token: newRefreshToken } = response.data

        // Update tokens
        setAccessToken(access_token)
        if (newRefreshToken) {
          setRefreshToken(newRefreshToken)
        }

        // Retry original request with new token
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`
        }

        return apiClient(originalRequest)
      } catch (refreshError) {
        // Refresh failed, redirect to login
        clearTokens()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

/**
 * API Error class for type-safe error handling
 */
export class ApiError extends Error {
  status: number
  code: string | undefined
  details: unknown | undefined

  constructor(message: string, status: number, code?: string, details?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = details
  }
}

/**
 * Extract error message from Axios error
 */
export function getErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    const data = error.response?.data as { detail?: string; message?: string } | undefined
    return data?.detail || data?.message || error.message
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'An unknown error occurred'
}

/**
 * Check if error is a network error (no response)
 */
export function isNetworkError(error: unknown): boolean {
  return error instanceof AxiosError && !error.response
}

/**
 * Check if error is authentication error (401)
 */
export function isAuthError(error: unknown): boolean {
  return error instanceof AxiosError && error.response?.status === 401
}

/**
 * Check if error is authorization error (403)
 */
export function isForbiddenError(error: unknown): boolean {
  return error instanceof AxiosError && error.response?.status === 403
}

/**
 * Check if error is not found error (404)
 */
export function isNotFoundError(error: unknown): boolean {
  return error instanceof AxiosError && error.response?.status === 404
}

export default apiClient
