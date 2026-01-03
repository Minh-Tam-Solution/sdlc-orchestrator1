/**
 * Authentication Hook - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useAuth
 * @description React hook for authentication state management
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 61 - Frontend Platform Consolidation
 */

"use client";

import { useState, useEffect, useCallback, createContext, useContext } from "react";
import type { ReactNode } from "react";
import { getCurrentUser, logout as apiLogout, refreshToken as apiRefreshToken } from "@/lib/api";
import type { UserProfile, TokenResponse } from "@/lib/api";

// Token storage keys
// NOTE: Existing landing/auth pages already persist tokens under these keys.
// Keep compatibility with any older prefixed keys during the spike.
const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const LEGACY_ACCESS_TOKEN_KEY = "sdlc_access_token";
const LEGACY_REFRESH_TOKEN_KEY = "sdlc_refresh_token";

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
 */
function getStoredAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return (
    localStorage.getItem(ACCESS_TOKEN_KEY) ||
    localStorage.getItem(LEGACY_ACCESS_TOKEN_KEY)
  );
}

/**
 * Get stored refresh token
 */
function getStoredRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return (
    localStorage.getItem(REFRESH_TOKEN_KEY) ||
    localStorage.getItem(LEGACY_REFRESH_TOKEN_KEY)
  );
}

/**
 * Store tokens in localStorage
 */
function storeTokens(accessToken: string, refreshToken: string): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);

  // Back-compat for any code paths still reading legacy keys.
  localStorage.setItem(LEGACY_ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(LEGACY_REFRESH_TOKEN_KEY, refreshToken);
}

/**
 * Clear stored tokens
 */
function clearTokens(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);

  localStorage.removeItem(LEGACY_ACCESS_TOKEN_KEY);
  localStorage.removeItem(LEGACY_REFRESH_TOKEN_KEY);
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
   * Fetch user profile with access token
   */
  const fetchUser = useCallback(async (accessToken: string): Promise<UserProfile | null> => {
    try {
      const user = await getCurrentUser(accessToken);
      return user;
    } catch (error) {
      console.error("Failed to fetch user:", error);
      return null;
    }
  }, []);

  /**
   * Initialize auth state on mount
   */
  useEffect(() => {
    const initAuth = async () => {
      const accessToken = getStoredAccessToken();

      if (!accessToken) {
        setState((prev) => ({ ...prev, isLoading: false }));
        return;
      }

      const user = await fetchUser(accessToken);

      if (user) {
        setState({
          user,
          isLoading: false,
          isAuthenticated: true,
          error: null,
        });
      } else {
        // Try to refresh token
        const refreshTokenValue = getStoredRefreshToken();
        if (refreshTokenValue) {
          try {
            const tokens = await apiRefreshToken(refreshTokenValue);
            storeTokens(tokens.access_token, tokens.refresh_token);
            const refreshedUser = await fetchUser(tokens.access_token);
            if (refreshedUser) {
              setState({
                user: refreshedUser,
                isLoading: false,
                isAuthenticated: true,
                error: null,
              });
              return;
            }
          } catch {
            // Refresh failed, clear tokens
            clearTokens();
          }
        }

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
   */
  const login = useCallback(async (tokens: TokenResponse) => {
    storeTokens(tokens.access_token, tokens.refresh_token);
    const user = await fetchUser(tokens.access_token);

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
   */
  const logout = useCallback(async () => {
    const accessToken = getStoredAccessToken();
    const refreshTokenValue = getStoredRefreshToken();

    if (accessToken && refreshTokenValue) {
      try {
        await apiLogout(accessToken, refreshTokenValue);
      } catch (error) {
        console.error("Logout API error:", error);
      }
    }

    clearTokens();
    setState({
      user: null,
      isLoading: false,
      isAuthenticated: false,
      error: null,
    });
  }, []);

  /**
   * Refresh authentication
   */
  const refreshAuth = useCallback(async (): Promise<boolean> => {
    const refreshTokenValue = getStoredRefreshToken();

    if (!refreshTokenValue) {
      return false;
    }

    try {
      const tokens = await apiRefreshToken(refreshTokenValue);
      storeTokens(tokens.access_token, tokens.refresh_token);
      const user = await fetchUser(tokens.access_token);

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
      clearTokens();
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
   */
  const getAccessToken = useCallback((): string | null => {
    return getStoredAccessToken();
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
