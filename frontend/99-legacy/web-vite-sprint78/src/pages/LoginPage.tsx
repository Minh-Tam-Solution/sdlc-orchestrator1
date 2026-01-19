/**
 * File: frontend/web/src/pages/LoginPage.tsx
 * Version: 1.2.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2026-01-18
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 5.1.3 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Login page for SDLC Orchestrator frontend.
 * Implements email/password authentication and OAuth (Google, GitHub).
 *
 * Design Reference:
 * docs/02-design/09-UI-Design/FRONTEND-DESIGN-SPECIFICATION.md
 * Page 1: Login Page (`/login`)
 *
 * Changelog:
 * - v1.2.0 (2026-01-18): Update to match design spec (Remember me, Forgot password, layout order)
 * - v1.1.0 (2026-01-18): Add Google and GitHub OAuth buttons
 * - v1.0.0 (2025-11-27): Initial implementation
 */

import { useState, FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'
import api from '@/api/client'

/**
 * Google Icon SVG component
 */
function GoogleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
    </svg>
  )
}

/**
 * GitHub Icon SVG component
 */
function GitHubIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
    </svg>
  )
}

/**
 * Login page component
 *
 * Design Spec Reference:
 * - docs/02-design/09-UI-Design/FRONTEND-DESIGN-SPECIFICATION.md
 * - Page 1: Login Page (`/login`)
 *
 * Features (per design):
 * - Email/password authentication
 * - Remember me checkbox
 * - Sign In button
 * - Separator "OR"
 * - Google OAuth login
 * - GitHub OAuth login
 * - Forgot password link
 *
 * @returns Login page component
 */
export default function LoginPage() {
  const navigate = useNavigate()
  const { login, isLoading, error, isAuthenticated } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const [oauthLoading, setOauthLoading] = useState<string | null>(null)

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault()

    try {
      await login({ email, password })
      // On success, redirect to dashboard
      navigate('/')
    } catch (err) {
      // Error is handled by AuthContext
      console.error('Login failed:', err)
    }
  }

  /**
   * Handle OAuth login
   */
  const handleOAuthLogin = async (provider: 'google' | 'github') => {
    try {
      setOauthLoading(provider)
      // Note: api client already has baseURL = /api/v1, so just use relative path
      const response = await api.get(`/auth/oauth/${provider}/authorize`)
      const { authorization_url } = response.data

      if (authorization_url) {
        // Redirect to OAuth provider
        window.location.href = authorization_url
      }
    } catch (err) {
      console.error(`${provider} OAuth failed:`, err)
      setOauthLoading(null)
    }
  }

  // If already authenticated, redirect to dashboard
  if (isAuthenticated) {
    navigate('/')
    return null
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-2xl font-bold">Sign In</CardTitle>
          <CardDescription>Welcome back</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            {/* Error message */}
            {error && (
              <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
                {error}
              </div>
            )}

            {/* Email field */}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                autoFocus
              />
            </div>

            {/* Password field */}
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
              />
            </div>

            {/* Remember me checkbox */}
            <div className="flex items-center space-x-2">
              <Checkbox
                id="rememberMe"
                checked={rememberMe}
                onCheckedChange={(checked) => setRememberMe(checked === true)}
              />
              <Label htmlFor="rememberMe" className="text-sm font-normal cursor-pointer">
                Remember me
              </Label>
            </div>

            {/* Sign In button */}
            <Button
              type="submit"
              className="w-full"
              disabled={isLoading || oauthLoading !== null || !email || !password}
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </Button>

            {/* Separator */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">
                  OR
                </span>
              </div>
            </div>

            {/* OAuth Buttons */}
            <Button
              type="button"
              variant="outline"
              onClick={() => handleOAuthLogin('google')}
              disabled={isLoading || oauthLoading !== null}
              className="w-full"
            >
              {oauthLoading === 'google' ? (
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-current border-t-transparent" />
              ) : (
                <GoogleIcon className="mr-2 h-5 w-5" />
              )}
              Google
            </Button>

            <Button
              type="button"
              variant="outline"
              onClick={() => handleOAuthLogin('github')}
              disabled={isLoading || oauthLoading !== null}
              className="w-full"
            >
              {oauthLoading === 'github' ? (
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-current border-t-transparent" />
              ) : (
                <GitHubIcon className="mr-2 h-5 w-5" />
              )}
              GitHub
            </Button>
          </CardContent>
          <CardFooter className="flex justify-center">
            <Link
              to="/forgot-password"
              className="text-sm text-muted-foreground hover:text-primary hover:underline"
            >
              Forgot password?
            </Link>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
