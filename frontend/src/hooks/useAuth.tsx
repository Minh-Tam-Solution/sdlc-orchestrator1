/**
 * Authentication Hook - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useAuth
 * @description React hook for authentication state management
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 63 - httpOnly Cookie Migration
 */

"use client";

import { useState, useEffect, useCallback, createContext, useContext } from "react";
import type { ReactNode } from "react";
import { getCurrentUser, logout as apiLogout, refreshToken as apiRefreshToken } from "@/lib/api";
import type { UserProfile, TokenResponse } from "@/lib/api";

// Sprint 63: httpOnly Cookie Authentication
// Tokens are stored in httpOnly cookies by backend (Set-Cookie headers)
// JavaScript cannot read httpOnly cookies - browser auto-includes them
// All token storage functions are no-ops for backward compatibility

interface AuthState {
  user: UserProfile | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}

interface AuthContextType extends AuthState {
  login: (tokens: TokenResponse) => Promise<void>;
  logout: () => Promise<void>;
  refreshAuth: () => Promise<boolean>;
  getAccessToken: () => string | null;
}

const AuthContext = createContext<AuthContextType | null>(null);

/**
 * Get stored access token
 * Sprint 63: NO-OP - Token is in httpOnly cookie, JavaScript cannot read it
 * Backend reads from Cookie header automatically via credentials: 'include'
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function getStoredAccessToken(): string | null {
  // httpOnly cookies cannot be read by JavaScript
  // Return null to indicate tokens are cookie-based
  return null;
}

/**
 * Get stored refresh token
 * Sprint 63: NO-OP - Token is in httpOnly cookie, JavaScript cannot read it
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function getStoredRefreshToken(): string | null {
  // httpOnly cookies cannot be read by JavaScript
  return null;
}

/**
 * Store tokens in localStorage
 * Sprint 63: NO-OP - Cookies are set by backend Set-Cookie headers
 * Keep function signature for backward compatibility
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function storeTokens(accessToken: string, refreshToken: string): void {
  // NO-OP: Backend sets httpOnly cookies via Set-Cookie headers
  // Browser automatically manages cookies
  // Keep function to avoid breaking login flow that calls this
}

/**
 * Clear stored tokens
 * Sprint 63: NO-OP - Backend clears cookies via Set-Cookie with Max-Age=0
 */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function clearTokens(): void {
  // NO-OP: Backend clears httpOnly cookies
  // Keep function to avoid breaking logout flow
}

/**
 * Auth Provider Component
 */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    error: null,
  });

  /**
   * Fetch user profile
   * Sprint 63: Uses httpOnly cookie for authentication
   */
  const fetchUser = useCallback(async (): Promise<UserProfile | null> => {
    try {
      const user = await getCurrentUser();
      return user;
    } catch (error) {
      console.error("Failed to fetch user:", error);
      return null;
    }
  }, []);

  /**
   * Initialize auth state on mount
   * Sprint 63: Check auth by calling /auth/me (cookie-based)
   */
  useEffect(() => {
    const initAuth = async () => {
      // Try to fetch user profile using httpOnly cookie
      const user = await fetchUser();

      if (user) {
        setState({
          user,
          isLoading: false,
          isAuthenticated: true,
          error: null,
        });
      } else {
        // No valid cookie or expired - user needs to login
        setState({
          user: null,
          isLoading: false,
          isAuthenticated: false,
          error: null,
        });
      }
    };

    initAuth();
  }, [fetchUser]);

  /**
   * Login with tokens (called after successful auth)
   * Sprint 63: Tokens are already set as httpOnly cookies by backend
   */
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const login = useCallback(async (tokens: TokenResponse) => {
    // Backend has already set httpOnly cookies via Set-Cookie headers
    // Just fetch user profile to update state
    const user = await fetchUser();

    if (user) {
      setState({
        user,
        isLoading: false,
        isAuthenticated: true,
        error: null,
      });
    } else {
      setState((prev) => ({
        ...prev,
        error: "Failed to fetch user profile",
      }));
    }
  }, [fetchUser]);

  /**
   * Logout and clear tokens
   * Sprint 63: Backend clears httpOnly cookies
   */
  const logout = useCallback(async () => {
    try {
      // Backend reads tokens from cookies and clears them
      await apiLogout();
    } catch (error) {
      console.error("Logout API error:", error);
    }

    // No need to clear localStorage - cookies are httpOnly
    setState({
      user: null,
      isLoading: false,
      isAuthenticated: false,
      error: null,
    });
  }, []);

  /**
   * Refresh authentication
   * Sprint 63: Backend reads refresh_token from httpOnly cookie
   */
  const refreshAuth = useCallback(async (): Promise<boolean> => {
    try {
      // Backend reads refresh_token cookie and sets new cookies
      await apiRefreshToken();
      const user = await fetchUser();

      if (user) {
        setState({
          user,
          isLoading: false,
          isAuthenticated: true,
          error: null,
        });
        return true;
      }
    } catch (error) {
      console.error("Token refresh failed:", error);
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        error: null,
      });
    }

    return false;
  }, [fetchUser]);

  /**
   * Get current access token
   * Sprint 63: Returns null - token is in httpOnly cookie
   */
  const getAccessToken = useCallback((): string | null => {
    // httpOnly cookies cannot be read by JavaScript
    // Token is automatically included in requests via credentials: 'include'
    return null;
  }, []);

  const value: AuthContextType = {
    ...state,
    login,
    logout,
    refreshAuth,
    getAccessToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access auth context
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}

/**
 * Hook to check if user has required role
 */
export function useHasRole(requiredRoles: string[]): boolean {
  const { user } = useAuth();

  if (!user || !user.roles) {
    return false;
  }

  return requiredRoles.some((role) => user.roles.includes(role));
}
