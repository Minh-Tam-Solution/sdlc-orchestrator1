/**
 * File: frontend/web/src/components/auth/ProtectedRoute.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Protected route wrapper that requires authentication.
 * Redirects unauthenticated users to login page.
 */

import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'

interface ProtectedRouteProps {
  children: React.ReactNode
}

/**
 * Protected route component
 *
 * Wraps routes that require authentication.
 * Redirects to login if user is not authenticated.
 * Preserves the attempted URL for redirect after login.
 *
 * @param children - Child components to render if authenticated
 * @returns Protected content or redirect to login
 */
export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth()
  const location = useLocation()

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    )
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    // Save the attempted URL for redirect after login
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}
