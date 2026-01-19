/**
 * File: frontend/web/src/components/layout/Header.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Header component with user menu and logout functionality.
 */

import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'

/**
 * Header component
 *
 * @returns Header with user info and logout button
 */
export default function Header() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  /**
   * Handle logout - clear tokens and redirect to login
   */
  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="fixed left-64 right-0 top-0 z-30 flex h-16 items-center justify-between border-b bg-background px-6">
      {/* Page title placeholder */}
      <div />

      {/* User menu */}
      <div className="flex items-center gap-4">
        {user && (
          <div className="text-sm">
            <span className="text-muted-foreground">Signed in as </span>
            <span className="font-medium">{user.email}</span>
          </div>
        )}
        <Button variant="outline" size="sm" onClick={handleLogout}>
          Sign Out
        </Button>
      </div>
    </header>
  )
}
