/**
 * File: frontend/web/src/contexts/AuthContext.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Authentication context for SDLC Orchestrator frontend.
 * Manages user authentication state, login/logout, and token refresh.
 */

import { createContext, useContext, useState, ReactNode } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import apiClient, {
  setTokens,
  clearTokens,
  getErrorMessage,
} from '@/api/client'
import {
  isAuthenticated as checkAuth,
  getUserId,
} from '@/utils/tokenManager'

/**
 * User interface (matches backend User model)
 */
export interface User {
  id: string
  username: string
  email: string
  name?: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  roles?: string[]
  oauth_providers?: string[]
  created_at: string
  updated_at: string
  last_login_at?: string
}

/**
 * Login credentials interface (matches backend LoginRequest)
 */
export interface LoginCredentials {
  email: string
  password: string
}

/**
 * Login response interface
 */
export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

/**
 * Auth context value interface
 */
export interface AuthContextValue {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  logout: () => void
  error: string | null
}

/**
 * Auth context
 */
const AuthContext = createContext<AuthContextValue | undefined>(undefined)

/**
 * Auth provider props
 */
export interface AuthProviderProps {
  children: ReactNode
}

/**
 * Auth provider component
 *
 * Provides authentication state and methods to entire application.
 * Automatically fetches user data if access token exists.
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [error, setError] = useState<string | null>(null)
  const queryClient = useQueryClient()

  // Check if user is authenticated on mount
  const isAuthenticated = checkAuth()
  const userId = getUserId()

  // Fetch current user if authenticated
  const { data: user, isLoading: userLoading } = useQuery<User>({
    queryKey: ['user', 'me'],
    queryFn: async () => {
      const response = await apiClient.get<User>('/auth/me')
      return response.data
    },
    enabled: isAuthenticated && !!userId,
    retry: false,
  })

  // Login mutation
  const loginMutation = useMutation<LoginResponse, Error, LoginCredentials>({
    mutationFn: async (credentials) => {
      const response = await apiClient.post<LoginResponse>('/auth/login', {
        email: credentials.email,
        password: credentials.password,
      })

      return response.data
    },
    onSuccess: (data) => {
      // Store tokens
      setTokens(data.access_token, data.refresh_token)

      // Refetch user data
      queryClient.invalidateQueries({ queryKey: ['user', 'me'] })

      // Clear error
      setError(null)
    },
    onError: (err) => {
      setError(getErrorMessage(err))
    },
  })

  // Login function
  const login = async (credentials: LoginCredentials): Promise<void> => {
    await loginMutation.mutateAsync(credentials)
  }

  // Logout function
  const logout = (): void => {
    clearTokens()
    queryClient.clear()
    setError(null)
  }

  const value: AuthContextValue = {
    user: user || null,
    isLoading: loginMutation.isPending || userLoading,
    isAuthenticated: isAuthenticated && !!user,
    login,
    logout,
    error: error || (loginMutation.error ? getErrorMessage(loginMutation.error) : null),
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

/**
 * Use auth hook
 *
 * @returns Auth context value
 * @throws Error if used outside AuthProvider
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }

  return context
}
