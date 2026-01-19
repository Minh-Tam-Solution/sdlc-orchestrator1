/**
 * File: frontend/web/src/utils/tokenManager.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Token management utilities for JWT authentication in SDLC Orchestrator.
 * Handles token storage, parsing, validation, and expiration checks.
 */

/**
 * JWT token payload interface
 */
export interface JwtPayload {
  sub: string // User ID
  exp: number // Expiration timestamp (Unix timestamp)
  iat: number // Issued at timestamp
  type: 'access' | 'refresh'
}

/**
 * Storage keys for tokens
 */
const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

/**
 * Parse JWT token without verification (client-side only for expiration check)
 *
 * SECURITY NOTE: This does NOT verify the token signature.
 * Token verification happens on the backend. This is only for client-side
 * checks like expiration to avoid unnecessary API calls.
 *
 * @param token - JWT token string
 * @returns Decoded JWT payload or null if invalid
 */
export function parseJwt(token: string): JwtPayload | null {
  try {
    const base64Url = token.split('.')[1]
    if (!base64Url) return null

    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      window
        .atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )

    return JSON.parse(jsonPayload) as JwtPayload
  } catch (error) {
    console.error('Failed to parse JWT token:', error)
    return null
  }
}

/**
 * Check if JWT token is expired
 *
 * @param token - JWT token string
 * @returns true if expired, false otherwise
 */
export function isTokenExpired(token: string): boolean {
  const payload = parseJwt(token)
  if (!payload?.exp) return true

  // Add 60 second buffer to refresh before actual expiration
  const now = Math.floor(Date.now() / 1000)
  return payload.exp - 60 < now
}

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
 * Check if user is authenticated (has valid access token)
 */
export function isAuthenticated(): boolean {
  const token = getAccessToken()
  if (!token) return false

  return !isTokenExpired(token)
}

/**
 * Get user ID from access token
 */
export function getUserId(): string | null {
  const token = getAccessToken()
  if (!token) return null

  const payload = parseJwt(token)
  return payload?.sub || null
}

/**
 * Get token expiration timestamp
 */
export function getTokenExpiration(token: string): number | null {
  const payload = parseJwt(token)
  return payload?.exp || null
}

/**
 * Get time until token expiration in seconds
 */
export function getTimeUntilExpiration(token: string): number | null {
  const exp = getTokenExpiration(token)
  if (!exp) return null

  const now = Math.floor(Date.now() / 1000)
  return Math.max(0, exp - now)
}
